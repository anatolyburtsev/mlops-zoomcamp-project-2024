# pylint: disable=duplicate-code

import json

import requests


def validate_metrics(metrics):
    assert 0 <= metrics["mse"] <= 1000, f"mse out of range: {metrics['mse']}"
    assert 0 <= metrics["mae"] <= 30, f"mae out of range: {metrics['mae']}"
    assert -1 <= metrics["r2"] <= 1, f"r2 out of range: {metrics['r2']}"


def main():
    event = {
        "intermediate_path": "s3://data/train_model_input.csv",
        "model_output_path": "s3://data/model",
    }

    url = "http://localhost:9001/2015-03-31/functions/function/invocations"
    actual_response = requests.post(url, json=event).json()
    print("Actual response:")
    print(json.dumps(actual_response, indent=2))

    # Extracting metrics from the response body
    if "body" in actual_response:
        body = json.loads(actual_response["body"])
        if "metrics" in body:
            metrics = body["metrics"]
            validate_metrics(metrics)
            print("Metrics are within the specified limits.")
        else:
            print("Metrics not found in the response body.")
    else:
        print("Invalid response format, 'body' key not found.")


if __name__ == "__main__":
    main()
