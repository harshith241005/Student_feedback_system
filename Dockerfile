FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY app /app/app
COPY templates /app/templates
COPY static /app/static
COPY tests /app/tests

ENV DATABASE_PATH=/app/data/feedback.db
RUN mkdir -p /app/data

EXPOSE 5000

CMD ["python", "app/app.py"]
