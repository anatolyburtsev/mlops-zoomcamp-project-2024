# Bike Duration Predictor Batch

This project provides a batch processing solution for predicting bike durations using AWS Lambda, Docker, and Poetry for dependency management. The `Makefile` includes targets for building and running Docker containers, installing dependencies, running tests, and more.

## Prerequisites

- Docker
- Docker Compose
- Poetry
- AWS CLI (for interacting with LocalStack)

## Makefile Targets

### Installation

- **install**: Installs dependencies including development dependencies.
  ```bash
  make install
  ```

- **install-prod**: Installs dependencies excluding development dependencies.
  ```bash
  make install-prod
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

## Integration Tests
script builds a Docker image for service, starts all necessary services using Docker Compose, 
uploads test data to a local S3 bucket in LocalStack, 
and calls the data processing Lambda function. 
It then downloads the processed output from S3 and
compares it with the expected output
```bash
integration_tests/run.sh
```