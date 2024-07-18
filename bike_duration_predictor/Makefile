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
	$(POETRY) run pre-commit install

# Install dependencies excluding dev
install-prod:
	$(POETRY) install --no-dev

# Delete Poetry environment
clean-env:
	$(POETRY) env remove --all

# Clean up coverage files
clean:
	rm -rf .coverage htmlcov

integration-test-data-processing:
	./integration_tests/run_data_processing.sh

integration-test-model-training:
	./integration_tests/run_model_training.sh

# Run all integration tests
integration-test-all: integration-test-data-processing integration-test-model-training

# Run pre-commit hooks manually
-hooks:
	$(POETRY) run pre-commit run --all-files
