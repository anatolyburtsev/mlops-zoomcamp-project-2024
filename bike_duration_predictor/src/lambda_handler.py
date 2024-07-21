import json
import os

import mlflow
from mlflow.models import infer_signature

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

    if not input_path:
        return {
            "status_code": 400,
            "body": json.dumps("Missing input_path or output_path"),
        }

    mlflow_ip = os.environ["MLFLOW_IP"]
    print(f"mlflow ip: {mlflow_ip}")
    mlflow.set_tracking_uri(f"http://{mlflow_ip}:5000")
    mlflow.set_experiment("bike-duration-prediction-2")

    input_bucket, input_key = parse_s3_path(input_path)
    print("Reading processed data from S3...")
    df = read_from_s3(input_bucket, input_key)

    print("Training model...")
    with mlflow.start_run():
        trained_model: TrainedModel = train_model(df)

        # Log parameters (if any)
        # mlflow.log_param("param_name", param_value)

        for metric_name, metric_value in trained_model.metrics.__dict__.items():
            mlflow.log_metric(metric_name, metric_value)

        # Infer the model signature
        signature = infer_signature(df.drop("duration_min", axis=1), df["duration_min"])

        # Log the model
        print("Logging the model")
        mlflow.sklearn.log_model(
            sk_model=trained_model.model,
            artifact_path="model",
            signature=signature,
            registered_model_name="bike-duration-predictor",
        )

        # Log the input data as an artifact
        temp_data_path = "/tmp/input_data.csv"
        df.to_csv(temp_data_path, index=False)
        mlflow.log_artifact(temp_data_path, "input_data")

        run_id = mlflow.active_run().info.run_id

    print("Model training and logging complete.")
    return json.dumps({"status_code": 200, "metrics": trained_model.metrics.__dict__, "mlflow_run_id": run_id})
