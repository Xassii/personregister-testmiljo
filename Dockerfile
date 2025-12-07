FROM python:3.14-slim

WORKDIR /app

RUN mkdir -p data
RUN mkdir -p tests

COPY requirements.txt .
COPY *.py .
COPY tests/*.py tests/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]