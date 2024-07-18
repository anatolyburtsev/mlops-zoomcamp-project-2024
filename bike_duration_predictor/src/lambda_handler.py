import json

import joblib

from .data_processing import process_data
from .train_model import TrainedModel, train_model
from .utils import parse_s3_path, read_from_s3, write_to_s3


def data_processing_lambda_handler(event, context):
    print(f"{event=}")
    input_path = event["input_path"]
    output_path = event["intermediate_path"]

    input_bucket, input_key = parse_s3_path(input_path)
    output_bucket, output_key = parse_s3_path(output_path)

    df = read_from_s3(input_bucket, input_key)
    processed_df = process_data(df)
    write_to_s3(processed_df, output_bucket, output_key)

    return json.dumps({"status_code": 200, "intermediate_path": output_path})


def model_train_lambda_handler(event, context):
    input_path = event.get("intermediate_path")
    output_path = event.get("model_output_path")

    if not input_path or not output_path:
        return {
            "status_code": 400,
            "body": json.dumps("Missing input_path or output_path"),
        }

    if not input_path.startswith("s3://") or not output_path.startswith("s3://"):
        return {
            "status_code": 400,
            "body": json.dumps("Paths must be S3 URLs starting with s3://"),
        }

    input_bucket, input_key = parse_s3_path(input_path)
    print("Reading processed data from S3...")
    df = read_from_s3(input_bucket, input_key)

    print("Training model...")
    trained_model: TrainedModel = train_model(df)

    model_file = "/tmp/model.pkl"
    metrics = trained_model.metrics.__dict__

    # Save the model to a temporary file
    joblib.dump(trained_model.model, model_file)

    # Write model and metrics to S3
    output_bucket, output_key_base = parse_s3_path(output_path)
    print("Uploading model and metrics to S3...")
    write_to_s3(model_file, output_bucket, f"{output_key_base}/model.pkl")
    write_to_s3(metrics, output_bucket, f"{output_key_base}/metrics.json")

    print("Model training complete.")

    return json.dumps({"status_code": 200, "metrics": metrics, "model_output_path": output_path})
