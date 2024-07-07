#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Set image names if not already set
if [ "${DATAPROCESSING_IMAGE_NAME}" == "" ]; then
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export DATAPROCESSING_IMAGE_NAME="bike_duration_predictor_dataprocessing:${LOCAL_TAG}"
    export MODELTRAINING_IMAGE_NAME="bike_duration_predictor_modeltraining:${LOCAL_TAG}"
    echo "DATAPROCESSING_IMAGE_NAME is not set, building a new image with tag ${DATAPROCESSING_IMAGE_NAME}"
    docker build -f ../dataprocessing.dockerfile -t ${DATAPROCESSING_IMAGE_NAME} ..
else
    echo "No need to build image ${DATAPROCESSING_IMAGE_NAME}"
fi

# Start Docker Compose setup
docker compose up -d data-processing localstack

echo "Wait for services to start"
sleep 5

# Upload test data to S3
export AWS_ACCESS_KEY_ID=abc
export AWS_SECRET_ACCESS_KEY=xyz
export AWS_DEFAULT_REGION=eu-west-1

aws --endpoint-url=http://localhost:4566 s3 mb s3://data
aws --endpoint-url=http://localhost:4566 s3 cp data/input.csv s3://data/input.csv

# Call data processing service
echo "Calling data processing service..."
python call_data_processing_lambda.py

# Compare output file with expected one
aws --endpoint-url=http://localhost:4566 s3 cp s3://data/output.csv temp_data/

diff temp_data/output.csv data/expected_output.csv
ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker compose logs
    docker compose down
    exit ${ERROR_CODE}
else
    echo "Data processing test passed"
fi

docker compose down
