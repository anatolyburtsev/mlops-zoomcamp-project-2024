# pylint: disable=duplicate-code

import json

import requests

event = {
    "input_path": "s3://data/input.csv",
    "intermediate_path": "s3://data/output.csv",
}

url = "http://localhost:9000/2015-03-31/functions/function/invocations"
actual_response = json.loads(requests.post(url, json=event).json())
print(f"{actual_response=}")

assert actual_response["status_code"] == 200
