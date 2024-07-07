import boto3

from .utils import read_from_s3, write_to_s3, parse_s3_path
from .data_processing import process_data
import json


def handler(event, context):
    print(f"{event=}")
    input_path = event['input_path']
    output_path = event['output_path']

    input_bucket, input_key = parse_s3_path(input_path)
    output_bucket, output_key = parse_s3_path(output_path)

    df = read_from_s3(input_bucket, input_key)
    processed_df = process_data(df)
    write_to_s3(processed_df, output_bucket, output_key)

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }