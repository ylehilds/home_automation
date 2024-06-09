from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json

authentication_scopes = [ "https://www.googleapis.com/auth/indexing" ]
publish_endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
metadata_endpoint = "https://indexing.googleapis.com/v3/urlNotifications/metadata"

json_key_file = "config.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key_file, scopes=authentication_scopes)
http = credentials.authorize(httplib2.Http())

index_url = input("What URL would you like to index? ")

payload = {
  "url": index_url,
  "type": "URL_UPDATED"
}

response, content = http.request(publish_endpoint, method="POST", body=json.dumps(payload))

if response.status == 200:
    print(f'The submission was successful. Google reported a {response.status} response code.')
else:
    print(f'The submission was not successful. Google reported a {response.status} response code, instead of 200.')