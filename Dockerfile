FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app
COPY data /app/data

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
