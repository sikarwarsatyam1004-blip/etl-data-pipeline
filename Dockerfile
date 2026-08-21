FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY airflow/dags ./dags
COPY tests ./tests

CMD ["pytest", "tests/"]