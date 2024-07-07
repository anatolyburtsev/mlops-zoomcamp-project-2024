# Variables
POETRY := poetry
PYTHON := $(POETRY) run python
COVERAGE := $(POETRY) run coverage
PYTEST := $(POETRY) run pytest
COVERAGE_THRESHOLD := 95

DATAPROCESSING_IMAGE_NAME = bike_duration_predictor_dataprocessing
MODELTRAINING_IMAGE_NAME = bike_duration_predictor_modeltraining
DOCKER_TAG = latest
DATAPROCESSING_CONTAINER_NAME = bike_duration_predictor_dataprocessing_container
MODELTRAINING_CONTAINER_NAME = bike_duration_predictor_modeltraining_container
DATAPROCESSING_PORT = 9000
MODELTRAINING_PORT = 9001
S3_ENDPOINT_URL = http://localstack:4566/

.PHONY: all install test lint clean docker-build docker-run docker-stop docker-rerun docker-build-dataprocessing docker-build-modeltraining docker-run-dataprocessing docker-run-modeltraining docker-stop-dataprocessing docker-stop-modeltraining docker-rerun-dataprocessing docker-rerun-modeltraining

# Default target
all: test

# Run tests with coverage
test:
	$(COVERAGE) run -m pytest

# Generate coverage report and enforce minimum coverage
coverage: test
	$(COVERAGE) report --fail-under=$(COVERAGE_THRESHOLD)
	$(COVERAGE) html

# Install dependencies including dev
install:
	$(POETRY) install

# Install dependencies excluding dev
install-prod:
	$(POETRY) install --no-dev

# Delete Poetry environment
clean-env:
	$(POETRY) env remove --all

# Clean up coverage files
clean:
	rm -rf .coverage htmlcov

# Build Docker images
docker-build: docker-build-dataprocessing docker-build-modeltraining

docker-build-dataprocessing:
	@echo "Building Docker image for data processing..."
	docker build -f dataprocessing.dockerfile -t $(DATAPROCESSING_IMAGE_NAME):$(DOCKER_TAG) .

docker-build-modeltraining:
	@echo "Building Docker image for model training..."
	docker build -f modeltraining.dockerfile -t $(MODELTRAINING_IMAGE_NAME):$(DOCKER_TAG) .

# Run Docker containers
docker-run: docker-run-dataprocessing docker-run-modeltraining

docker-run-dataprocessing:
	@echo "Running Docker container for data processing..."
	-docker stop $(DATAPROCESSING_CONTAINER_NAME) || true
	-docker rm $(DATAPROCESSING_CONTAINER_NAME) || true
	docker run -d --name $(DATAPROCESSING_CONTAINER_NAME) -p $(DATAPROCESSING_PORT):8080 -e S3_ENDPOINT_URL=$(S3_ENDPOINT_URL) -e AWS_ACCESS_KEY_ID=foobar -e AWS_SECRET_ACCESS_KEY=foobar $(DATAPROCESSING_IMAGE_NAME):$(DOCKER_TAG)

docker-run-modeltraining:
	@echo "Running Docker container for model training..."
	-docker stop $(MODELTRAINING_CONTAINER_NAME) || true
	-docker rm $(MODELTRAINING_CONTAINER_NAME) || true
	docker run -d --name $(MODELTRAINING_CONTAINER_NAME) -p $(MODELTRAINING_PORT):8080 -e S3_ENDPOINT_URL=$(S3_ENDPOINT_URL) -e AWS_ACCESS_KEY_ID=foobar -e AWS_SECRET_ACCESS_KEY=foobar $(MODELTRAINING_IMAGE_NAME):$(DOCKER_TAG)

# Stop Docker containers
docker-stop: docker-stop-dataprocessing docker-stop-modeltraining

docker-stop-dataprocessing:
	@echo "Stopping Docker container for data processing..."
	-docker stop $(DATAPROCESSING_CONTAINER_NAME)
	-docker rm $(DATAPROCESSING_CONTAINER_NAME)

docker-stop-modeltraining:
	@echo "Stopping Docker container for model training..."
	-docker stop $(MODELTRAINING_CONTAINER_NAME)
	-docker rm $(MODELTRAINING_CONTAINER_NAME)

# Rerun Docker containers
docker-rerun: docker-stop docker-build docker-run

docker-rerun-dataprocessing: docker-stop-dataprocessing docker-build-dataprocessing docker-run-dataprocessing

docker-rerun-modeltraining: docker-stop-modeltraining docker-build-modeltraining docker-run-modeltraining

integration-test-data-processing:
	./integration_tests/run_data_processing.sh

# Run model training integration test
integration-test-model-training:
	./integration_tests/run_model_training.sh

# Run all integration tests
integration-test-all: integration-test-data-processing integration-test-model-training
