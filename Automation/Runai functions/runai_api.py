import json
import requests


class RunaiClient:
    def __init__(self, tenant_name: str, cluster_id: str, client_id: str, client_secret: str,
                 runai_base_url: str, verify_cert: bool):
        self.cluster_id = cluster_id
        self._base_url = f"{runai_base_url}/v1/k8s"
        self._verify_cert = verify_cert
        self.default_user = default_user
        self._api_token = self._get_api_token(runai_base_url, tenant_name, client_id, client_secret)

    @property
    def _request_headers(self):
        return {"authorization": f"Bearer {self._api_token}", 'content-type': "application/json"}

    def _get_api_token(self, runai_base_url: str, tenant_name: str, client_id: str, client_secret: str):
        payload = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
        headers = {'content-type': "application/x-www-form-urlencoded"}
        url = f"{runai_base_url}/auth/realms/{tenant_name}/protocol/openid-connect/token"
        try:
            response = requests.post(url, payload, headers=headers, verify=self._verify_cert)
            response.raise_for_status()
            response_json = response.json()
            if "access_token" not in response_json:
                raise SystemExit(f"failed to get access token from response. response body={response_json}")

            return response_json["access_token"]

        except requests.exceptions.HTTPError as err:
            print(f"failed to get api token. err={err}")
            raise SystemExit(err)
        except requests.exceptions.JSONDecodeError as err:
            print(f"failed to decode json response. err={err}")
            raise SystemExit(err)

    def get_all_departments(self):
        return self._get(f"clusters/{self.cluster_id}/departments")

    def get_all_projects(self):
        return self._get(f"clusters/{self.cluster_id}/projects")

    def get_all_users(self):
        return self._get("users")

    def create_user(self, new_user_body: dict):
        return self._post("users", data=new_user_body)

    def create_project(self, new_project_body: dict):
        return self._post(f"clusters/{self.cluster_id}/projects", new_project_body)

    def create_department(self, new_department_body: dict):
        return self._post(f"clusters/{self.cluster_id}/departments", new_department_body)

    def update_project(self, project_id, updated_project_body):
        return self._put(f"clusters/{self.cluster_id}/projects/{project_id}", updated_project_body)

    def delete_project(self, project_id):
        return self._delete(f"clusters/{self.cluster_id}/projects/{project_id}")

    def get_node_pools(self):
        return self._get(f"clusters/{self.cluster_id}/nodepools")

    def _get(self, url: str):
        try:
            response = requests.get(f"{self._base_url}/{url}",
                                    headers=self._request_headers,
                                    verify=self._verify_cert)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"error when trying to _get from url {url}. err={err}")
            raise SystemExit(err)

    def _post(self, url: str, data: dict):
        try:
            response = requests.post(f"{self._base_url}/{url}",
                                     data=json.dumps(data),
                                     headers=self._request_headers,
                                     verify=self._verify_cert)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"error when trying to _post to url {url}, with data={data}. err={err}")
            raise SystemExit(err)

    def _put(self, url: str, data: dict):
        try:
            response = requests.put(f"{self._base_url}/{url}",
                                    data=json.dumps(data),
                                    headers=self._request_headers,
                                    verify=self._verify_cert)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"error when trying to _put to url {url}, with data={data}. err={err}")
            raise SystemExit(err)

    def _delete(self, url: str):
        try:
            response = requests.delete(f"{self._base_url}/{url}",
                                      headers=self._request_headers,
                                      verify=self._verify_cert)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
            print(f"error when trying to _delete to url {url}, with err={err}")


