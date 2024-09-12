# Flask Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY flask-server/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY flask-server/ .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
