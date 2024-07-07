#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Set image names if not already set
if [ "${MODELTRAINING_IMAGE_NAME}" == "" ]; then
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export DATAPROCESSING_IMAGE_NAME="bike_duration_predictor_dataprocessing:${LOCAL_TAG}"
    export MODELTRAINING_IMAGE_NAME="bike_duration_predictor_modeltraining:${LOCAL_TAG}"
    echo "MODELTRAINING_IMAGE_NAME is not set, building a new image with tag ${MODELTRAINING_IMAGE_NAME}"
    docker build -f ../modeltraining.dockerfile -t ${MODELTRAINING_IMAGE_NAME} ..
else
    echo "No need to build image ${MODELTRAINING_IMAGE_NAME}"
fi

# Start Docker Compose setup for model training and localstack only
docker compose up -d model-training localstack

echo "Wait for services to start"
sleep 5

# Upload test data to S3
export AWS_ACCESS_KEY_ID=abc
export AWS_SECRET_ACCESS_KEY=xyz
export AWS_DEFAULT_REGION=eu-west-1

aws --endpoint-url=http://localhost:4566 s3 mb s3://data
aws --endpoint-url=http://localhost:4566 s3 cp data/train_model_input.csv s3://data/train_model_input.csv

# Call model training service
echo "Calling model training service..."
python call_model_training_lambda.py

# Validate that metrics and model were saved to S3 and are not empty
aws --endpoint-url=http://localhost:4566 s3 cp s3://data/model/metrics.json temp_data/
aws --endpoint-url=http://localhost:4566 s3 cp s3://data/model/model.pkl temp_data/

if [ ! -s temp_data/metrics.json ]; then
    echo "Metrics file is empty or not found!"
    docker compose logs
    docker compose down
    exit 1
fi

if [ ! -s temp_data/model.pkl ]; then
    echo "Model file is empty or not found!"
    docker compose logs
    docker compose down
    exit 1
fi

echo "Model training test passed"

docker compose down
