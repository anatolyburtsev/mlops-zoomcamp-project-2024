# Variables
POETRY := poetry
PYTHON := $(POETRY) run python
COVERAGE := $(POETRY) run coverage
PYTEST := $(POETRY) run pytest
COVERAGE_THRESHOLD := 95

IMAGE_NAME = bike_duration_predictor_batch
DOCKER_TAG = latest
CONTAINER_NAME = bike_duration_predictor_container
PORT = 9000
S3_ENDPOINT_URL = http://localstack:4566/

.PHONY: all install test lint clean docker-build docker-run docker-stop


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

docker-build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME):$(DOCKER_TAG) .

docker-run:
	@echo "Running Docker container..."
	-docker stop $(CONTAINER_NAME) || true
	-docker rm $(CONTAINER_NAME) || true
	docker run --name $(CONTAINER_NAME) -p $(PORT):8080 -e S3_ENDPOINT_URL=$(S3_ENDPOINT_URL) -e AWS_ACCESS_KEY_ID=foobar -e AWS_SECRET_ACCESS_KEY=foobar $(IMAGE_NAME):$(DOCKER_TAG)

docker-stop:
	@echo "Stopping Docker container..."
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

docker-rerun: docker-stop docker-build docker-run