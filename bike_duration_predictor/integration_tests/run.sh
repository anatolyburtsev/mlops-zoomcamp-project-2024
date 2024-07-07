#!/usr/bin/env bash

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export LOCAL_IMAGE_NAME="bike-duration-dataprocessing:${LOCAL_TAG}"
    echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
    docker build -t ${LOCAL_IMAGE_NAME} ..
else
    echo "no need to build image ${LOCAL_IMAGE_NAME}"
fi

docker compose up -d

sleep 5

# upload test data to S3
export AWS_ACCESS_KEY_ID=foobar
export AWS_SECRET_ACCESS_KEY=foobar
export AWS_DEFAULT_REGION=us-east-1

aws --endpoint-url=http://localhost:4566 s3 mb s3://data
aws --endpoint-url=http://localhost:4566 s3 cp input.csv s3://data/input.csv

echo "Calling data processing lambda..."
python call_data_processing_lambda.py

# compare output file with expected one
aws --endpoint-url=http://localhost:4566 s3 cp s3://data/output.csv .

diff output.csv expected_output.csv
ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker compose logs
    docker compose down
    exit ${ERROR_CODE}
else
    echo "Test passed"
fi


docker compose down