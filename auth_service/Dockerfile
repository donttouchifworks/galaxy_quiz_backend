FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/bin/sh", "-c", "if [ \"$ENVIRONMENT\" = \"prod\" ]; then gunicorn -w 4 -b 0.0.0.0:8001 app:app; else flask run --host=0.0.0.0 --port=8001 --debug --reload; fi"]
