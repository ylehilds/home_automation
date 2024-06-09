import requests

## Secrets
import config
import urls

## Bing Info
bing_submission_url = "https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey="
bing_api_key = config.api_key
bing_submission_urls = { "siteUrl":"https://lehi.dev", "urlList":urls.submission_url_list } #Create URL list to submit to Bing.
headers = { "Content-Type": "application/json; charset=utf-8" } #Bing response headers.

## Make request to Bing.
submission_request = requests.post(f"{bing_submission_url}{bing_api_key}", headers=headers, json=bing_submission_urls)

if submission_request.status_code == 200:
    print("Submission to Bing was successful.")
else:
    print("Submission was not successful or daily limit is reached. Please try again.")
