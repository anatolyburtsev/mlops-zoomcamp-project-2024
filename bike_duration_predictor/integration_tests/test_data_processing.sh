#!/bin/bash

export AWS_ACCESS_KEY_ID=foobar
export AWS_SECRET_ACCESS_KEY=foobar
export AWS_DEFAULT_REGION=us-east-1

aws --endpoint-url=http://localhost:4566 s3 mb s3://data

aws --endpoint-url=http://localhost:4566 s3 cp input.csv s3://data/input.csv

