import http.client
from pip._vendor import requests
import json

# Application Name and Secret must be created in the Run:AI User Interface. See https://docs.run.ai/developer/rest-auth/
APPNAME = '<APP NAME>'
APPSECRET = '<APP SECRET>'
# the URL is the URL to the Run:AI User Interface
APPURL = 'https://<RUNAI URL>'
# REALM is obtained by going to the Run:AI User Interface, Settings > General and getting the REALM from the client configuration under "Researcher Authentication"
REALM = '<REALM>'

def login():
    payload = "grant_type=client_credentials&client_id=" + APPNAME + "&client_secret=" + APPSECRET
    headers = { 'content-type': 'application/x-www-form-urlencoded'    }
    url = APPURL + '/auth/realms/' + REALM + '/protocol/openid-connect/token'

    r = requests.post(url, headers=headers, data=payload)

    if r.status_code //100 == 2:
        jcontents = json.loads(r.text)
        print (jcontents['access_token'])
        return 
    
    else:
        print("login error: " + r.text)
        exit(1)
        
login()