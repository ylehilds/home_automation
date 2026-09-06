#!/usr/bin/env bash

# Local control for legacy Belkin Wemo devices.
#
# Usage:
#   ./wemo_control.sh <IP-or-network> <on|off|getstate|getsignal|getname|find>
#
# Examples:
#   ./wemo_control.sh 192.168.50.141 on
#   ./wemo_control.sh 192.168.50.141 getstate
#   ./wemo_control.sh '192.168.50.*' find

set -u
set -o pipefail

readonly SCRIPT_NAME="$(basename "$0")"
readonly USAGE="Usage: $SCRIPT_NAME <IP-or-network> <on|off|getstate|getsignal|getname|find>"

# Wemo models commonly use one of these ports.  The script discovers the
# active one from setup.xml instead of assuming a fixed port.
readonly DEFAULT_PORTS="49152 49153 49154 49155 49156 49157 49158 49159"

IP=""
PORT=""

die() {
    echo "Error: $*" >&2
    exit 1
}

usage() {
    echo "$USAGE" >&2
    exit 2
}

require_command() {
    command -v "$1" >/dev/null 2>&1 || die "required command not found: $1"
}

validate_target() {
    # Prevent accidental option injection or malformed URLs.  This accepts
    # IPv4 addresses, host names, and an nmap-style network for find.
    [[ "$1" =~ ^[A-Za-z0-9_.:*+-]+$ ]] ||
        die "invalid device address or network: $1"
}

discover_port() {
    local candidate ports status
    ports="${WEMO_PORTS:-$DEFAULT_PORTS}"

    if [[ -n "${WEMO_PORT:-}" ]]; then
        [[ "$WEMO_PORT" =~ ^[0-9]+$ ]] &&
            (( WEMO_PORT >= 1 && WEMO_PORT <= 65535 )) ||
            die "WEMO_PORT must be a number from 1 to 65535"
        PORT="$WEMO_PORT"
        return 0
    fi

    for candidate in $ports; do
        status="$(curl --silent --output /dev/null \
            --connect-timeout 2 --max-time 5 --http1.0 \
            --write-out '%{http_code}' \
            "http://$IP:$candidate/setup.xml" 2>/dev/null)" ||
            status="000"

        if [[ "$status" == "200" ]]; then
            PORT="$candidate"
            return 0
        fi
    done

    die "could not find a Wemo service on $IP; tried ports: $ports"
}

soap_request() {
    local action="$1"
    local body="$2"
    local url="http://$IP:$PORT/upnp/control/basicevent1"
    local response status payload

    response="$(printf '%s' "$body" | curl --silent --show-error \
        --connect-timeout 2 --max-time 8 --http1.0 \
        -H 'Accept:' \
        -H 'Content-Type: text/xml; charset="utf-8"' \
        -H "SOAPACTION: \"urn:Belkin:service:basicevent:1#$action\"" \
        --data-binary @- \
        --write-out $'\n__WEMO_HTTP_STATUS__:%{http_code}' \
        "$url")" || {
        die "HTTP request failed for $url"
    }

    status="${response##*$'\n__WEMO_HTTP_STATUS__:'}"
    payload="${response%$'\n__WEMO_HTTP_STATUS__:'*}"

    [[ "$status" =~ ^2[0-9][0-9]$ ]] || {
        echo "$payload" >&2
        die "Wemo returned HTTP $status for SOAP action $action"
    }

    if grep -Eqi '<(s:)?Fault([ >]|$)' <<<"$payload"; then
        echo "$payload" >&2
        die "Wemo returned a SOAP fault for action $action"
    fi

    printf '%s' "$payload"
}

extract_tag() {
    local tag="$1"
    # Wemo responses are small XML documents. Normalize line breaks before
    # extracting the first matching element without requiring xmllint.
    tr '\r\n' '  ' |
        sed -n "s:.*<${tag}[^>]*>\\([^<]*\\)</${tag}>.*:\\1:p" |
        head -n 1
}

get_state() {
    local response state
    response="$(soap_request "GetBinaryState" \
'<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
 s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:GetBinaryState xmlns:u="urn:Belkin:service:basicevent:1">
      <BinaryState>1</BinaryState>
    </u:GetBinaryState>
  </s:Body>
</s:Envelope>')"

    state="$(printf '%s' "$response" | extract_tag BinaryState)"
    case "$state" in
        0) echo "OFF" ;;
        1) echo "ON" ;;
        *) die "unexpected GetBinaryState response: $state" ;;
    esac
}

set_state() {
    local requested="$1"
    local value response state

    case "$requested" in
        on) value=1 ;;
        off) value=0 ;;
        *) die "internal error: invalid state $requested" ;;
    esac

    response="$(soap_request "SetBinaryState" \
"<?xml version=\"1.0\" encoding=\"utf-8\"?>
<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\"
 s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">
  <s:Body>
    <u:SetBinaryState xmlns:u=\"urn:Belkin:service:basicevent:1\">
      <BinaryState>$value</BinaryState>
    </u:SetBinaryState>
  </s:Body>
</s:Envelope>")"

    state="$(printf '%s' "$response" | extract_tag BinaryState)"
    case "$state" in
        0) echo "OFF" ;;
        1) echo "ON" ;;
        *)
            # Some Wemo firmware returns an empty SOAP result for a
            # successful SetBinaryState. Confirm with a follow-up query.
            get_state
            ;;
    esac
}

get_name() {
    local response name
    response="$(soap_request "GetFriendlyName" \
'<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
 s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:GetFriendlyName xmlns:u="urn:Belkin:service:basicevent:1">
      <FriendlyName></FriendlyName>
    </u:GetFriendlyName>
  </s:Body>
</s:Envelope>')"

    name="$(printf '%s' "$response" | extract_tag FriendlyName)"
    [[ -n "$name" ]] && echo "$name" || die "Wemo returned an empty friendly name"
}

get_signal_strength() {
    local response strength
    response="$(soap_request "GetSignalStrength" \
'<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
 s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:GetSignalStrength xmlns:u="urn:Belkin:service:basicevent:1">
      <GetSignalStrength>0</GetSignalStrength>
    </u:GetSignalStrength>
  </s:Body>
</s:Envelope>')"

    strength="$(printf '%s' "$response" | extract_tag SignalStrength)"
    [[ -n "$strength" ]] && echo "$strength" || die "Wemo returned no signal strength"
}

find_devices() {
    local device name device_port
    require_command nmap

    echo "Scanning $IP for Wemo devices..." >&2
    while read -r device; do
        [[ -n "$device" ]] || continue
        IP="$device"
        PORT=""
        if discover_port 2>/dev/null; then
            device_port="$PORT"
            name="$(get_name 2>/dev/null || echo unknown)"
            printf '%-16s %-6s %s\n' "$device" "$device_port" "$name"
        fi
    done < <(nmap -n -p 49152-49159 --open "$IP" -oG - 2>/dev/null |
        awk '/Ports:/{print $2}')
}

main() {
    local command

    [[ "$#" -eq 2 ]] || usage
    require_command curl
    IP="$1"
    # Use tr instead of Bash 4's ${var,,}; macOS commonly ships Bash 3.2.
    command="$(printf '%s' "$2" | tr '[:upper:]' '[:lower:]')"
    validate_target "$IP"

    if [[ "$command" == "find" ]]; then
        find_devices
        return 0
    fi

    case "$command" in
        on|off|getstate|getsignal|getsignalstrength|getname|getfriendlyname) ;;
        *) usage ;;
    esac

    discover_port

    case "$command" in
        on|off) set_state "$command" ;;
        getstate) get_state ;;
        getsignal|getsignalstrength) get_signal_strength ;;
        getname|getfriendlyname) get_name ;;
        *) usage ;;
    esac
}

main "$@"
