import json
import os
from io import BytesIO, StringIO
from typing import Union
from urllib.parse import urlparse

import boto3
import joblib
import pandas as pd
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def parse_s3_path(s3_path):
    parsed_url = urlparse(s3_path, allow_fragments=False)
    bucket = parsed_url.netloc
    key = parsed_url.path.lstrip("/")
    return bucket, key


def read_from_local(path):
    return pd.read_csv(path)


def write_to_local(data: Union[pd.DataFrame, dict, object], path: str):
    """Writes data to a local file. The data can be a Pandas DataFrame, a dictionary (JSON), or a serialized model.

    Args:
    ----
        data (Union[pd.DataFrame, dict, object]): The data to be saved. Can be a DataFrame, a JSON serializable dict, or a model.
        path (str): The path to the file in the local filesystem.

    """
    try:
        if isinstance(data, pd.DataFrame):
            data.to_csv(path, index=False)
        elif isinstance(data, dict):
            with open(path, "w") as f:
                json.dump(data, f)
        else:
            joblib.dump(data, path)
        print(f"Successfully wrote to {path}")
    except Exception as e:
        print(f"Failed to write to local file: {e}")


def read_from_s3(bucket, key):
    """Reads a CSV file from an S3 bucket.

    Args:
    ----
        bucket (str): The name of the S3 bucket.
        key (str): The key (path) to the CSV file in the S3 bucket.

    Returns:
    -------
        pd.DataFrame: The loaded DataFrame.

    """
    s3 = create_s3_client()
    response = s3.get_object(Bucket=bucket, Key=key)
    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        csv_string = response["Body"].read().decode("utf-8")
        df = pd.read_csv(StringIO(csv_string))
        return df
    else:
        raise Exception(f"Unsuccessful S3 get_object response. Status - {status}")


def write_to_s3(data: Union[pd.DataFrame, dict, object], bucket: str, key: str):
    """Writes data to an S3 bucket. The data can be a Pandas DataFrame, a dictionary (JSON), or a serialized model.

    Args:
    ----
        data (Union[pd.DataFrame, dict, object]): The data to be saved. Can be a DataFrame, a JSON serializable dict, or a model.
        bucket (str): The name of the S3 bucket.
        key (str): The key (path) to the file in the S3 bucket.

    """
    s3 = create_s3_client()
    try:
        if isinstance(data, pd.DataFrame):
            csv_buffer = StringIO()
            data.to_csv(csv_buffer, index=False)
            s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
        elif isinstance(data, dict):
            json_buffer = json.dumps(data)
            s3.put_object(Bucket=bucket, Key=key, Body=json_buffer)
        else:
            model_buffer = BytesIO()
            joblib.dump(data, model_buffer)
            model_buffer.seek(0)  # Reset buffer position to the beginning
            s3.put_object(Bucket=bucket, Key=key, Body=model_buffer.getvalue())
        print(f"Successfully wrote {key} to bucket {bucket}")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {e}")
    except Exception as e:
        print(f"Failed to write to S3: {e}")


def create_s3_client():
    endpoint_url = os.getenv("S3_ENDPOINT_URL")
    print(f"{endpoint_url=}")

    if endpoint_url is None:
        return boto3.client("s3")

    return boto3.client("s3", endpoint_url=endpoint_url)
