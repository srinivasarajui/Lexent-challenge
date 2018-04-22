import sys
import requests
import json

baseURL = 'http://127.0.0.1:5000/'
headers = {'Content-Type': 'application/json'}

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        sys.exit("use python Client.py jobFilePath")
    path = sys.argv[1]
    with open(path) as json_data:
      data = json.load(json_data)
      response = requests.post('{0}SubmitJob'.format(baseURL), headers=headers, json=data)

