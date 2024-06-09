from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json

## Secrets
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..','..'))
import config

authentication_scopes = [ "https://www.googleapis.com/auth/indexing" ]
publish_endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
metadata_endpoint = "https://indexing.googleapis.com/v3/urlNotifications/metadata"

credentials = ServiceAccountCredentials.from_json_keyfile_dict(config.google_api_key, scopes=authentication_scopes)
http = credentials.authorize(httplib2.Http())

index_url = input("What URL would you like to index? ")

payload = {
  "url": index_url,
  "type": "URL_UPDATED"
}

response, content = http.request(publish_endpoint, method="POST", body=json.dumps(payload))

if response.status == 200:
    print(f'The submission was successful. Google reported a {response.status} response code for url: {index_url}.')
else:
    print(f'The submission was not successful. Google reported a {response.status} response code, instead of 200 for url: {index_url}.')