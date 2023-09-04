import http.client
from pip._vendor import requests
import json
import random
import string


# Application Name and Secret must be created in the Run:AI User Interface. See https://docs.run.ai/developer/rest-auth/
APPNAME = '<APP NAME>'
APPSECRET = '<APP SECRET>'
# the URL is the URL to the Run:AI User Interface
APPURL = 'https://<RUNAI URL>'
# REALM is obtained by going to the Run:AI User Interface, Settings > General and getting the REALM from the client configuration under "Researcher Authentication"
REALM = '<REALM>'
# The department feature is advanced and is mostly disabled. 
# Find out the default department ID by listing departments via https://app.run.ai/api/docs/#/Departments/get_v1_k8s_departments (Usually is 1)
DEPARTMENT_ID = '<DEPARTMENT_ID>'  
# A tenant (customer) may define multiple clusters. 
# Find out the Cluster UUID by logging into the Administraor user interface and go to "Clusters"
CLUSTER_UUID = '<CLUSTER_UUID>'
# Base name and email domain to be combined for usernames
USERDEFAULT = "john"
EMAILDOMAIN = "@acme.com"
# Base project name to be used
PROJECTDEFAULT = "john-project"
# GPU Allowance for each project
GPUDEFAULT = '<GPU ALLOWANCE>'
# No. of users and projects to create
QUANTITY = '<QUANTITY>'


#Generate a random password of fixed length 
def randomString(stringLength):
    letters = string.ascii_letters
    digits = string.digits
    return ''.join(random.choice(letters) for i in range(stringLength)) + random.choice(digits) + random.choice(string.punctuation)

def login():
    payload = "grant_type=client_credentials&client_id=" + APPNAME + "&client_secret=" + APPSECRET
    headers = { 'content-type': 'application/x-www-form-urlencoded'    }
    url = APPURL + '/auth/realms/' + REALM + '/protocol/openid-connect/token'

    r = requests.post(url, headers=headers, data=payload)

    if r.status_code //100 == 2:
        jcontents = json.loads(r.text)
        return jcontents['access_token']
    
    else:
        print("login error: " + r.text)
        exit(1)

def create_researcher_user(uid, pwd, token):

    payload = {
        "roles":["researcher"],
        "permittedClusters":[],
        "name":"",
        "password":pwd,
        "email":uid,
        "permitAllClusters":True,
        "username":uid,
        "needToChangePassword":True
    }
    
    jsonpayload = json.dumps(payload, separators=(',', ':'))

    headers = \
        {'content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    r = requests.post(APPURL + '/v1/k8s/users', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        jcontents = json.loads(r.text)
        return jcontents['userId']
    
    else:
        print("login error: " + r.text)
        exit(1)

def create_project(projectname, internalUID, gpuquota, token):
    payload = {
        "name":projectname,
        "departmentId":DEPARTMENT_ID,
        "deservedGpus":gpuquota,
        "clusterUuid":CLUSTER_UUID,
        "nodeAffinity":{"train":{"affinityType":"no_limit"},"interactive":{"affinityType":"no_limit"}},
        "permissions":{"users":[internalUID]}
    }
    
    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    headers = \
        {'content-type': 'application/json', 
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)
        }
    r = requests.post(APPURL + '/v1/k8s/clusters/' + CLUSTER_UUID + '/projects', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        jcontents = json.loads(r.text)
        return jcontents['id']
    
    else:
        print("create project error: " + r.text)
        exit(1)

def user_setup(username, emaildomain, projectname, gpuquota):
    access_token = login()    
    for i in range(QUANTITY):
        pwd = randomString(10)
        usr = username + str(i) + emaildomain
        prjtname = projectname + str(i)
        internalUID = create_researcher_user(usr, pwd, access_token)
        print("Username: " + usr + " Password: " + pwd)
        create_project(prjtname, internalUID, gpuquota, access_token)
        print("Projectname: " + prjtname + " GPU Quota: " + str(gpuquota))   
    return

# Create users, with their own Run:AI project and a quota of GPUs.
user_setup(USERDEFAULT, EMAILDOMAIN, PROJECTDEFAULT, GPUDEFAULT)