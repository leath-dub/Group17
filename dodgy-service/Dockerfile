
FROM python:3.9-slim

RUN apt-get update && apt-get install -y stress-ng && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY static ./static

EXPOSE 5000

CMD ["python", "app.py"]
