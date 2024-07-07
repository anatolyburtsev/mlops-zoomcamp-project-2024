FROM public.ecr.aws/lambda/python:3.12

COPY pyproject.toml ${LAMBDA_TASK_ROOT}/
COPY poetry.lock ${LAMBDA_TASK_ROOT}/
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

COPY src ${LAMBDA_TASK_ROOT}/src

CMD ["src.lambda_handler.data_processing_lambda_handler"]
