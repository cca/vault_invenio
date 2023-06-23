import json
import requests

# shut up urllib3 SSL verification warning
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

token = 'L7yvVDVBMJ8wx0WPVgXbQ2C83xTQNxO2yyvSHeKr9lU1fdIg0S5nX0Fy1sOd'
# at least 5 HTTP requests to creating an item with a single attachment:
# 1) create metadata record as draft
# 2) for each attachment
#   a) add file names to draft (could this be combined with the step above?)
#   b) add file data to draft
#   c) commit the file to the draft
# 3) publish the draft

def result(response):
    print('HTTP {}'.format(response.status_code))
    print(response.text)


with open('record.json', 'r') as fh:
    data = json.load(fh)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
    # create metadata-only draft
    response = requests.post('https://127.0.0.1/api/records', json=data, verify=False, headers=headers)

result(response)
draft = response.json()
id = draft['id']

# add file names to draft
file_keys = [{"key": "syllabus.pdf"}]
response = requests.post('https://127.0.0.1/api/records/{}/draft/files'.format(id), json=file_keys, headers=headers, verify=False)
result(response)

# PUT file data to draft
with open ('syllabus.pdf', 'rb') as file:
    headers['Content-Type'] = 'application/octet-stream'
    response = requests.put('https://127.0.0.1/api/records/{}/draft/files/{}/content'.format(id, 'syllabus.pdf'), data=file, headers=headers, verify=False)
    result(response)

# commit file
headers['Content-Type']= 'application/json'
response = requests.post('https://127.0.0.1/api/records/{}/draft/files/{}/commit'.format(id, 'syllabus.pdf'), headers=headers, verify=False)
result(response)

# publish draft
response = requests.post('https://127.0.0.1/api/records/{}/draft/actions/publish'.format(id), headers=headers, verify=False)
result(response)
# link to (HTML version of) published record
print(json.loads(response.text)['links']['self_html'])
