import requests

def get_token():
    url = 'https://{runai_base_url}/auth/realms/{tenant_name}/protocol/openid-connect/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': 'openid',
        'response_type': 'id_token',
        'client_id': {client_id},
        'client_secret': {client_secret},
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    token = response.json()['access_token']
    return token

def create_object(token, name):
    url = 'https://{runai_base_url}/v1/k8s/clusters/{cluster_UUID}/projects'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    data = {
        "name": name,
        "nodePoolsResources": [
            {
                "nodePool": {
                    "id": 1,
                    "name": "default"
                },
                "gpu": {
                    "deserved": 0,
                    "maxAllowed": 1000,
                    "overQuotaWeight": 2
                }
            }
        ],
        "namespace": f"runai-{name}",
        "departmentId": {department_id},
        "deservedGpus": 1,
        "maxAllowedGpus": 5,
        "gpuOverQuotaWeight": 1,
        "swapEnabled": False,
        "defaultNodePools": [
            "default"
        ],
        "interactiveJobTimeLimitSecs": 3600,
        "interactiveJobMaxIdleDurationSecs": 3000,
        "interactivePreemptibleJobMaxIdleDurationSecs": 3000,
        "trainingJobTimeLimitSecs": 3600,
        "trainingJobMaxIdleDurationSecs": 3000,
        "nodeAffinity": {
            "train": {
                "affinityType": "no_limit",
                "selectedTypes": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ]
            },
            "interactive": {
                "affinityType": "no_limit",
                "selectedTypes": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ]
            }
        },
        "permissions": {
            "users": [
                "string"
            ],
            "groups": [
                "string"
            ],
            "applications": [
                "string"
            ]
        },
        "resources": {
            "id": 0,
            "gpu": {
                "deserved": 0,
                "maxAllowed": 1000,
                "overQuotaWeight": 2
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print("Request failed")
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")
    response.raise_for_status()
    return response.json()

def main():
    name = input("Enter the name for the new namespace: ")
    token = get_token()
    result = create_object(token, name)
    phase = result.get('phase', 'No phase information available')
    print(f"Creation phase: {phase}")

if __name__ == '__main__':
    main()
