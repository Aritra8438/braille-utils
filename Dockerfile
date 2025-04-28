FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt .

RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY /api/ ./api
COPY /uploads/ ./uploads

RUN pip install waitress

EXPOSE 10000

CMD ["python", "api/index.py"]