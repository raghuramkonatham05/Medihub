FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y tesseract-ocr poppler-utils && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 10000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]