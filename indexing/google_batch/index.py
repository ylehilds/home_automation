from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build 
import httplib2

## Secrets
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..','..'))
import config

#urls
import urls

requests = urls.submission_url_list
  
SCOPES = [ "https://www.googleapis.com/auth/indexing" ]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
 
# Authorize credentials
credentials = ServiceAccountCredentials.from_json_keyfile_dict(config.google_api_key, scopes=SCOPES)
http = credentials.authorize(httplib2.Http())
 
# Build service
service = build('indexing', 'v3', credentials=credentials)
 
def insert_event(request_id, response, exception):
    if exception is not None:
        print(exception)
    else:
        print(response)
 
batch = service.new_batch_http_request(callback=insert_event)
 
for url, api_type in requests.items():
    batch.add(service.urlNotifications().publish(
        body={"url": url, "type": api_type}))
 
batch.execute()