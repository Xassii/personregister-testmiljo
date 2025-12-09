FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
COPY *.py .
COPY tests/*.py tests/

RUN mkdir -p data && \
    pip install -r requirements.txt

CMD ["python", "-u", "app.py"]