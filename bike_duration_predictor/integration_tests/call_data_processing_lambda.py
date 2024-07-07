# pylint: disable=duplicate-code

import json

import requests
from deepdiff import DeepDiff

event = {
   'input_path': 's3://data/input.csv',
   'output_path': 's3://data/output.csv',
}

url = 'http://localhost:9000/2015-03-31/functions/function/invocations'
actual_response = requests.post(url, json=event).json()
print('actual response:')

print(json.dumps(actual_response, indent=2))

expected_response = {
        'statusCode': 200,
        'body': '"Processing complete"'
    }


diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(f'diff={diff}')


