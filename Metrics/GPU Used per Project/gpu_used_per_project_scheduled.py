import csv
import requests
import datetime

# Set the URL and headers for the API call
APPURL = "<RUNAI_UI_URL>"
APPSECRET = "<GRAFANA_API_KEY>"


# Make the API call
url = APPURL + "/grafana/api/datasources/proxy/1/api/v1/query?query=runai_gpu_utilization_per_project"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + APPSECRET,
}
response = requests.get(url, headers=headers)

# Check if the API call was successful
if response.status_code != 200:
    print(f"API call failed with status code {response.status_code}")
    exit()

# Parse the JSON response
json_data = response.json()

# Get the project names
project_names = set()
for result in json_data["data"]["result"]:
    project_names.add(result["metric"]["project"])
project_names = sorted(list(project_names))

# Open the CSV file in append mode
with open("gpu_utilization_per_project.csv", "a+", newline="") as csvfile:
    writer = csv.writer(csvfile)

    # Check if the CSV file is empty
    csvfile.seek(0)
    first_char = csvfile.read(1)
    is_empty = not first_char

    # Write the header row if the CSV file is empty
    if is_empty:
        writer.writerow(["timestamp"] + project_names)

    # Write the utilization data for each project
    timestamp = datetime.datetime.now()
    utilization_dict = {result["metric"]["project"]: result["value"][1] for result in json_data["data"]["result"]}
    row = [timestamp]
    for project_name in project_names:
        if project_name in utilization_dict:
            row.append(utilization_dict[project_name])
        else:
            row.append("")
    writer.writerow(row)

print("Data written to gpu_utilization_per_project.csv")