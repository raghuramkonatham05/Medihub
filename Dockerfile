FROM python:3.10-slim

WORKDIR /app

# Install system dependencies

RUN apt-get update && apt-get install -y 
tesseract-ocr 
poppler-utils 
libgl1 
&& rm -rf /var/lib/apt/lists/*

# Copy project files

COPY . .

# Install Python packages

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port

EXPOSE 10000

# Start application

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
