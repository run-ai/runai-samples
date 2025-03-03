import http.client
from pip._vendor import requests
import json

# Application Name and Secret must be created in the Run:AI User Interface. See https://docs.run.ai/developer/rest-auth/
APPNAME = '<RUN:AI APPLICATION USER>'
APPSECRET = '<RUN:AI APPLICATION SECRET>'
# the URL is the URL to the Run:AI User Interface
APPURL = '<APPLICATION URL>'
# REALM is obtained by going to the Run:AI User Interface, and getting the REALM and "Researcher Authentication"
REALM = 'runai'
CLUSTERNAME = '<RUN:AI CLUSTER NAME>'
PROJECTNAME1 = '<RUN:AI PROJECT NAME>'
PROJECTNAME2 = '<RUN:AI PROJECT NAME>'
PROJECTNAME3 = '<RUN:AI PROJECT NAME>'
PROJECTNAME4 = '<RUN:AI PROJECT NAME>'

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

def get_projectid(token,pname):

    headers = \
        {'content-type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    r = requests.get(APPURL + '/api/v1/org-unit/projects', headers=headers)
 
    if r.status_code //100 == 2:
        jcontents = json.loads(r.text)
        projects = jcontents["projects"]
        for project in projects:
            if project["name"]== pname:
                return project["id"]
    else:
        print("login error: " + r.text)
        

def create_workload1(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "lee-train1",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 8,
            }
        }
    }

    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 1 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload2(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "lee-train2",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 4,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 2 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload3(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "almir-train1",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 1,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 3 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload4(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "wes-train1",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 4,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 4 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload5(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "wes-train2",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 2,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 5 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload6(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "wes-train3",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 2,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 6 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload7(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "rob-train1",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 2,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 7 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload8(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "rob-train2",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 1,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 8 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload9(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "rob-train3",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 1,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 9 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload10(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "steve-train1",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 2,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 10 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload11(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "steve-train2",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 1,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 11 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload12(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "steve-train3",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 1,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 12 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_workload13(token,pid,cid):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
        "name": "steve-train4",
        "projectId": pid,
        "clusterId": cid,
        "spec": {
            "image": "gcr.io/run-ai-demo/quickstart-demo",
            "compute": {
            "gpuDevicesRequest": 1,
            }
        }
    }


    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/workloads/trainings', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Workload 13 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def newworkload():
    access_token = login()
    cluster_id = get_clusterid(access_token)
    project1_id = get_projectid(access_token,PROJECTNAME1)
    project2_id = get_projectid(access_token,PROJECTNAME2)
    project3_id = get_projectid(access_token,PROJECTNAME3)
    project4_id = get_projectid(access_token,PROJECTNAME4)
    create_workload1(access_token,project2_id,cluster_id)
    create_workload2(access_token,project2_id,cluster_id)
    create_workload3(access_token,project3_id,cluster_id)
    create_workload4(access_token,project1_id,cluster_id)
    create_workload5(access_token,project3_id,cluster_id)
    create_workload6(access_token,project3_id,cluster_id)
    create_workload7(access_token,project3_id,cluster_id)
    create_workload8(access_token,project3_id,cluster_id)
    create_workload9(access_token,project4_id,cluster_id)
    create_workload10(access_token,project3_id,cluster_id)
    create_workload11(access_token,project4_id,cluster_id)
    create_workload12(access_token,project4_id,cluster_id)
    create_workload13(access_token,project4_id,cluster_id)
    return

# Create New Workload
newworkload()
