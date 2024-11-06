from pip._vendor import requests
import json
import re

# Application Name and Secret must be created in the Run:AI User Interface. See https://docs.run.ai/developer/rest-auth/
APPNAME = '<AppName>'
APPSECRET = '<AppSecret>'
# the URL is the URL to the Run:AI User Interface
APPURL = 'https://<Domain>'
# REALM is obtained by going to the Run:AI User Interface, and getting the REALM under "Researcher Authentication"
REALM = 'runai'
# CLUSTERNAME is obtained by going to the Run:AI User Interface, and getting the cluster name under "clusters"
CLUSTERNAME = '<ClusterName>'

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

def get_clusterid(token):

    headers = \
        {'content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    r = requests.get(APPURL + '/v1/k8s/clusters', headers=headers)
 
    if r.status_code //100 == 2:
        jcontents = json.loads(r.text)
        for item in jcontents:
            if item["name"]== CLUSTERNAME:
                clusteruuid = item["uuid"]
        return clusteruuid
    else:
        print("login error: " + r.text)
        exit(1)

def get_environments(token,clusterid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
        
    payload = {"clusterUuid": clusterid}
    
    r = requests.get(APPURL + '/api/v1/asset/environment', headers=headers, data=payload)
    
    # Parse the JSON response
    json_data = r.json()
 
    if r.status_code //100 == 2:     
        with open("environments.json", "wb") as file:
            file.write(r.content)
            print("Environments saved to environments.json")
        
        # define re pattern to define Json Object start
        pattern = r'{"meta.*?]}}'
        # open environments json file
        with open("environments.json", "r") as file:
            file_cont = file.read()
        # find all JSON Objects from a file by passing re pattern
        json_objs = re.findall(pattern, file_cont)
            
        # parse each JSON object
        i = 0
        for obj_string in json_objs:
            i += 1
            obj = json.loads(obj_string)
            #remove unneeded keys
            remove_a_key(obj, 'id')
            remove_a_key(obj, 'tenantId')
            remove_a_key(obj, 'kind')
            remove_a_key(obj, 'createdAt')
            remove_a_key(obj, 'createdBy')
            remove_a_key(obj, 'updatedAt')
            remove_a_key(obj, 'updatedBy')
            #create a config file for each environment
            with open("environment" + str(i) + ".json", "w") as file2:
                json.dump(obj, file2)          

    else:
        print("Create Failed: " + r.text)
        exit(1)        

def remove_a_key(d, remove_key):
    if isinstance(d, dict):
        for key in list(d.keys()):
            if key == remove_key:
                del d[key]
            else:
                remove_a_key(d[key], remove_key)
        
def start():
    access_token = login()
    clusterid = get_clusterid(access_token)   
    get_environments(access_token,clusterid)
    return

# Get Environments
start()
