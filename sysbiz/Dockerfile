FROM python:3.9-slim

WORKDIR /sysbiz
RUN pip install poetry
COPY pyproject.toml poetry.lock* /sysbiz/
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
COPY . /sysbiz/
CMD ["python", "sysbiz/main.py"]