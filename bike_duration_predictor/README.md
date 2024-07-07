# Bike Duration Predictor Batch

This project provides a batch processing solution for predicting bike durations using AWS Lambda, Docker, and Poetry for dependency management. The `Makefile` includes targets for building and running Docker containers, installing dependencies, running tests, and more.

## Prerequisites

- Docker
- Docker Compose
- Poetry
- AWS CLI (for interacting with LocalStack)

## Makefile Targets

### Installation

- **install**: Installs dependencies including development dependencies and pre-commit hooks
  ```bash
  make install
  ```

- **install-prod**: Installs dependencies excluding development dependencies.
  ```bash
  make install-prod
  ```
  
- **run-hooks**: run pre-commit hooks manually
  ```bash
  make run-hooks
  ```
 

### Testing

- **test**: Runs tests with coverage.
  ```bash
  make test
  ```

- **coverage**: Generates a coverage report and enforces a minimum coverage threshold.
  ```bash
  make coverage
  ```

### Cleaning

- **clean-env**: Deletes the Poetry environment.
  ```bash
  make clean-env
  ```

- **clean**: Cleans up coverage files.
  ```bash
  make clean
  ```

### Docker

- **docker-build**: Builds the Docker image.
  ```bash
  make docker-build
  ```

- **docker-run**: Runs the Docker container.
  ```bash
  make docker-run
  ```

- **docker-stop**: Stops the Docker container.
  ```bash
  make docker-stop
  ```

- **docker-rerun**: Stops the Docker container, rebuilds the Docker image, and runs the container.
  ```bash
  make docker-rerun
  ```

Here's an updated section of your README to reflect the integration tests for both data processing and model training:

## Integration Tests

### Data Processing Integration Test
This script builds the Docker image for the data processing service, starts the necessary services using Docker Compose, uploads test data to a local S3 bucket in LocalStack, calls the data processing Lambda function, downloads the processed output from S3, and compares it with the expected output.
```bash
make integration-test-data-processing
```

### Model Training Integration Test
This script builds the Docker image for the model training service, starts the necessary services using Docker Compose, uploads test data to a local S3 bucket in LocalStack, calls the model training Lambda function, and validates that the metrics and model were saved to S3 and are not empty.
```bash
make integration-test-model-training
```

### Run All Integration Tests
This command runs both the data processing and model training integration tests sequentially.
```bash
make integration-test-all
```
