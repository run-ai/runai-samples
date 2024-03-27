import http.client
from pip._vendor import requests
import json

# Application Name and Secret must be created in the Run:AI User Interface. See https://docs.run.ai/developer/rest-auth/
APPNAME = '<AppName>'
APPSECRET = '<AppSecret>'
# the URL is the URL to the Run:AI User Interface
APPURL = 'https://<Domain>'
# REALM is obtained by going to the Run:AI User Interface, and getting the REALM and "Researcher Authentication"
REALM = 'runai'
S3_ACCESSKEY = '<AccessKey>'
S3_SECRET = '<Secret>'
S3_URL = '<S3 URL>'
S3_BUCKET_NAME = '<S3 Bucket Name>'

def login():
    payload = "grant_type=client_credentials&client_id=" + APPNAME + "&client_secret=" + APPSECRET
    headers = { 'content-type': 'application/x-www-form-urlencoded' }
    url = APPURL + '/auth/realms/' + REALM + '/protocol/openid-connect/token'
z
    r = requests.post(url, headers=headers, data=payload)

    if r.status_code //100 == 2:
        jcontents = json.loads(r.text)
        return jcontents['access_token']
    
    else:
        print("login error: " + r.text)
        exit(1)

def create_credential1(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "s3key",
        "scope": "tenant"
    },
    "spec": {
            "accessKeyId": S3_ACCESSKEY,
            "secretAccessKey": S3_SECRET,
        }
    }

    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/credentials/access-key', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("S3 Demo Credentials Created Successfully")
        jcontents = json.loads(r.text)
        return jcontents['meta']['id']
        
  
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_datastore1(token,credid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "s3-example",
        "scope": "tenant",
    },
    "spec": {
            "bucket": S3_BUCKET_NAME,
            "path": "/home/jovyan/s3",
            "accessKeyAssetId": credid,
            "url": S3_URL,
        }
    }

    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/datasource/s3', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("S3 Example Datasource Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)
        
def create_datastore2(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "runai-samples",
        "scope": "tenant"
    },
    "spec": {
            "repository": "https://github.com/run-ai/runai-samples.git",
            "branch": "main",
            "path": "/home/jovyan/github"
    }
    }

    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/datasource/git', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Run:ai Samples Datasource Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)
        
def create_datastore3(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "rstudio-connect",
        "scope": "tenant",
    },
    "spec": {
            "repository": "https://github.com/rstudio/connect-examples.git",
            "branch": "main",
            "path": "/home/rstudio"
    }
    }

    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/datasource/git', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("RStudio Connect Datasource Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)
                
def newdatastores():
    access_token = login()    
    cred_id = create_credential1(access_token)
    create_datastore1(access_token,cred_id)
    create_datastore2(access_token)
    create_datastore3(access_token)
    return

# Create New Environment
newdatastores()
