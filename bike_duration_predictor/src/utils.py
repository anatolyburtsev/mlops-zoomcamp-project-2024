import os
from urllib.parse import urlparse

import boto3
import pandas as pd
from io import StringIO


def parse_s3_path(s3_path):
    parsed_url = urlparse(s3_path, allow_fragments=False)
    bucket = parsed_url.netloc
    key = parsed_url.path.lstrip('/')
    return bucket, key


def read_from_local(path):
    return pd.read_csv(path)


def write_to_local(df, path):
    df.to_csv(path, index=False)


def read_from_s3(bucket, key):
    """
    Reads a CSV file from an S3 bucket.

    Args:
        bucket (str): The name of the S3 bucket.
        key (str): The key (path) to the CSV file in the S3 bucket.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    s3 = create_s3_client()
    response = s3.get_object(Bucket=bucket, Key=key)
    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        csv_string = response["Body"].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_string))
        return df
    else:
        raise Exception(f"Unsuccessful S3 get_object response. Status - {status}")


def write_to_s3(df, bucket, key):
    """
    Writes a DataFrame to a CSV file in an S3 bucket.

    Args:
        df (pd.DataFrame): The DataFrame to be saved.
        bucket (str): The name of the S3 bucket.
        key (str): The key (path) to the CSV file in the S3 bucket.
    """
    s3 = create_s3_client()
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())


def create_s3_client():
    endpoint_url = os.getenv('S3_ENDPOINT_URL')
    print(f"{endpoint_url=}")

    if endpoint_url is None:
        return boto3.client('s3')

    return boto3.client('s3', endpoint_url=endpoint_url)
