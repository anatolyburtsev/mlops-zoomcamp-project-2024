## Development notes.
Mlflow auto start currently doesn't work, login to the machine and run
```shell
mlflow server --backend-store-uri sqlite:////mlflow/mlflow.db --default-artifact-root s3://mlflow-data-bucket-723351182543-us-west-2/mlflow-artifacts/ --host 0.0.0.0 --port 5000 &
```