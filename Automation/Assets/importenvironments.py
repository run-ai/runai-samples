from pip._vendor import requests
import json
import os

# Application Name and Secret must be created in the Run:AI User Interface. See https://docs.run.ai/developer/rest-auth/
APPNAME = '<AppName>'
APPSECRET = '<AppSecret>'
# the URL is the URL to the Run:AI User Interface
APPURL = 'https://<Domain>'
# REALM is obtained by going to the Run:AI User Interface, and getting the REALM under "Researcher Authentication"
REALM = 'runai'

def login():
    payload = "grant_type=client_credentials&client_id=" + APPNAME + "&client_secret=" + APPSECRET
    headers = { 'content-type': 'application/x-www-form-urlencoded' }
    url = APPURL + '/auth/realms/' + REALM + '/protocol/openid-connect/token'

    r = requests.post(url, headers=headers, data=payload)

    if r.status_code //100 == 2:
        jcontents = json.loads(r.text)
        return jcontents['access_token']
    
    else:
        print("login error: " + r.text)
        exit(1)

def create_environments(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    
    # Opening all environment JSON files in current folder sequentially
    i = 1
    while os.path.exists("environment" + str(i) + ".json"):
        payload = open("environment" + str(i) + ".json")
        # Import Environment
        r = requests.post(APPURL + '/api/v1/asset/environment', headers=headers, data=payload)

        if r.status_code //100 == 2:
            print("Environment " + str(i) + " Created Successfully")
            i += 1    
        else:
            print("Environment " + str(i) + " Create Failed: " + r.text)
            i += 1
            exit(1)
    
    else:
        print("Import Finished")
        return
        
        
def importenvironment():
    access_token = login()    
    create_environments(access_token)
    return

# import New Environment
importenvironment()
