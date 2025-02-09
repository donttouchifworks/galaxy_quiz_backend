FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/bin/sh", "-c", "if [ \"$ENVIRONMENT\" = \"prod\" ]; then gunicorn -w 4 -b 0.0.0.0:8000 --worker-class=gthread --threads 4 'app:create_app()'; else flask run --host=0.0.0.0 --port=8000 --reload --debug; fi"]

