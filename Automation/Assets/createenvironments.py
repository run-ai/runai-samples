import http.client
from pip._vendor import requests
import json

# Application Name and Secret must be created in the Run:AI User Interface. See https://docs.run.ai/developer/rest-auth/
APPNAME = '<APP USERNAME>'
APPSECRET = '<APP SECRET>'
# the URL is the URL to the Run:AI User Interface
APPURL = 'https://<DOMAIN URL>'
# REALM is obtained by going to the Run:AI User Interface, and getting the REALM and "Researcher Authentication"
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

def create_environment1(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "jupyter-example",
        "scope": "tenant",
        "workloadSupportedTypes": {
            "workspace": True,
            "training": True
        }
    },
    "spec": {
        "command": "start-notebook.sh",
        "args": "--NotebookApp.token=''",
        "environmentVariables": [],
        "image": "gcr.io/run-ai-demo/jupyter-demo",
        "imagePullPolicy": "IfNotPresent",
        "connections": [
            {
                "name": "Jupyter",
                "internalToolInfo": {
                    "toolType": "jupyter-notebook",
                    "connectionType": "ExternalUrl",
                    "containerPort": 8888,
                    "externalUrlInfo": {}
                }
            }
        ],
        "uidGidSource": "fromTheImage",
        "capabilities": []
    }
    }

    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/environment', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Environment 1 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)
        
def create_environment2(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "mlflow-example",
        "scope": "tenant",
        "workloadSupportedTypes": {
            "workspace": True,
            "training": True
        },
    },
    "spec": {
        "command": "bash -c \"bash -c 'mlflow server --host 0.0.0.0 &' & start-notebook.sh --NotebookApp.token=''\"",
        "environmentVariables": [],
        "image": "cubeist/jupyter-mlflow",
        "imagePullPolicy": "IfNotPresent",
        "connections": [
            {
                "name": "MLflow",
                "internalToolInfo": {
                    "toolType": "mlflow",
                    "connectionType": "ExternalUrl",
                    "containerPort": 5000,
                    "externalUrlInfo": {}
                }
            },
            {
                "name": "Jupyter",
                "internalToolInfo": {
                    "toolType": "jupyter-notebook",
                    "connectionType": "ExternalUrl",
                    "containerPort": 8888,
                    "externalUrlInfo": {}
                }
            }
        ],
        "uidGidSource": "fromTheImage",
        "capabilities": []
    }
    } 
    

    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/environment', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Environment 2 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_environment3(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "rstudio-example",
        "scope": "tenant",
        "workloadSupportedTypes": {
            "workspace": True,
            "training": True
        },
    },
    "spec": {
        "environmentVariables": [
            {
                "name": "DISABLE_AUTH",
                "value": "true"
            }
        ],
        "image": "rocker/rstudio:4",
        "imagePullPolicy": "IfNotPresent",
        "connections": [
            {
                "name": "RStudio",
                "internalToolInfo": {
                    "toolType": "rstudio",
                    "connectionType": "ExternalUrl",
                    "containerPort": 8787,
                    "externalUrlInfo": {}
                }
            }
        ],
        "uidGidSource": "fromTheImage",
        "capabilities": [
            "FOWNER",
            "CHOWN",
            "DAC_OVERRIDE",
            "SYS_CHROOT",
            "FSETID",
            "SETGID",
            "SETUID"
        ]
    }
    }

    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/environment', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Environment 3 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_environment4(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "vscode-example",
        "scope": "tenant",
        "workloadSupportedTypes": {
            "workspace": True,
            "training": True
        },
    },
    "spec": {
        "environmentVariables": [],
        "image": "quay.io/opendatahub-contrib/workbench-images:vscode-datascience-c9s-py311_2023c_latest",
        "imagePullPolicy": "IfNotPresent",
        "connections": [
            {
                "name": "VSCode",
                "internalToolInfo": {
                    "toolType": "visual-studio-code",
                    "connectionType": "ExternalUrl",
                    "containerPort": 8787,
                    "externalUrlInfo": {}
                }
            }
        ],
        "uidGidSource": "fromTheImage",
        "capabilities": []
    }
    }

    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/environment', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Environment 4 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)
        
def create_environment5(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "distributed-pytorch-example",
        "scope": "tenant",
        "workloadSupportedTypes": {
            "workspace": False,
            "training": True,
            "distributed": True,
            "distFramework": "PyTorch"
        },
    },
    "spec": {
        "environmentVariables": [],
        "image": "kubeflow/tf-mnist-with-summaries:latest",
        "imagePullPolicy": "IfNotPresent",
        "uidGidSource": "fromTheImage",
        "capabilities": []
    }
    }

    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/environment', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Environment 5 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)
        
def create_environment6(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "training-example",
        "scope": "tenant",
        "workloadSupportedTypes": {
            "training": True
        },
    },
    "spec": {
        "environmentVariables": [],
        "image": "gcr.io/run-ai-demo/quickstart-demo",
        "imagePullPolicy": "IfNotPresent",
        "uidGidSource": "fromTheImage",
        "capabilities": []
    }
    }

    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/environment', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Environment 6 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)
        
def create_environment7(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "matlab-example",
        "scope": "tenant",
        "workloadSupportedTypes": {
            "workspace": True,
            "training": True
        },
    },
    "spec": {
        "environmentVariables": [],
        "image": "mathworks/matlab",
        "imagePullPolicy": "IfNotPresent",
        "connections": [
            {
                "name": "MATLAB",
                "internalToolInfo": {
                    "toolType": "matlab",
                    "connectionType": "ExternalUrl",
                    "containerPort": 8888,
                    "externalUrlInfo": {}
                }
            }
        ],
        "uidGidSource": "fromTheImage",
        "capabilities": []
    }
    }
    
    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/environment', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Environment 7 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)
        
def create_environment8(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "wandb-jupyter-example",
        "scope": "tenant",
        "workloadSupportedTypes": {
            "workspace": True,
            "training": True
        },
    },
    "spec": {
        "command": "start-notebook.sh",
        "args": "--NotebookApp.token=\"\"",
        "environmentVariables": [
            {
                "name": "WANDB_PROJECT",
                "value": "rob-demo"
            },
            {
                "name": "WANDB_API_KEY",
                "value": "a22f27d89aec7de8419a4d0841bdbc9fef90a112"
            }
        ],
        "image": "jupyter/base-notebook",
        "imagePullPolicy": "IfNotPresent",
        "connections": [
            {
                "name": "Weights & Biases",
                "isExternal": True,
                "externalToolInfo": {
                    "toolType": "wandb",
                    "externalUrl": "https://wandb.ai/rob-magno/${WANDB_PROJECT}"
                }
            },
            {
                "name": "Jupyter",
                "internalToolInfo": {
                    "toolType": "jupyter-notebook",
                    "connectionType": "ExternalUrl",
                    "containerPort": 8888,
                    "externalUrlInfo": {}
                }
            }
        ],
        "uidGidSource": "fromTheImage",
        "capabilities": []
    }
    }
    
    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/environment', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Environment 8 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)

def create_environment9(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "jupyter-pytorch-ngc-example",
        "scope": "tenant",
        "workloadSupportedTypes": {
            "workspace": True,
            "training": True
        },
    },
    "spec": {
        "command": "jupyter",
        "args": "lab --NotebookApp.token=''",
        "environmentVariables": [],
        "image": "nvcr.io/nvidia/pytorch:23.08-py3",
        "imagePullPolicy": "IfNotPresent",
        "connections": [
            {
                "name": "Jupyter",
                "internalToolInfo": {
                    "toolType": "jupyter-notebook",
                    "connectionType": "ExternalUrl",
                    "containerPort": 8888,
                    "externalUrlInfo": {}
                }
            }
        ],
        "uidGidSource": "fromTheImage",
        "capabilities": []
    }
    }
    
    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/environment', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Environment 9 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)
        
def create_environment10(token):

    headers = \
        {'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)}
    payload = {
    "meta": {
        "name": "tf-tensorboard-example",
        "scope": "tenant",
        "workloadSupportedTypes": {
            "workspace": True,
            "training": True,
            "distributed": False
        },
    },
    "spec": {
        "command": "tensorboard",
        "args": "--logdir ./ --host 0.0.0.0",
        "environmentVariables": [],
        "image": "tensorflow/tensorflow:latest",
        "imagePullPolicy": "IfNotPresent",
        "connections": [
            {
                "name": "TensorBoard",
                "internalToolInfo": {
                    "toolType": "tensorboard",
                    "connectionType": "ExternalUrl",
                    "containerPort": 6006,
                    "externalUrlInfo": {}
                }
            }
        ],
        "uidGidSource": "fromTheImage",
        "capabilities": []
    }
    }
    
    jsonpayload = json.dumps(payload, separators=(',', ':'))
    
    r = requests.post(APPURL + '/api/v1/asset/environment', headers=headers, data=jsonpayload)
 
    if r.status_code //100 == 2:
        print("Environment 10 Created Successfully")      
    else:
        print("Create Failed: " + r.text)
        exit(1)
        
def newenvironment():
    access_token = login()    
    create_environment1(access_token)
    create_environment2(access_token)
    create_environment3(access_token)
    create_environment4(access_token)
    create_environment5(access_token)
    create_environment6(access_token)
    create_environment7(access_token)
    create_environment8(access_token)
    create_environment9(access_token)
    create_environment10(access_token)
    return

# Create New Environment
newenvironment()
