# Use an official Python runtime as the base image
FROM python:3.11-slim

# Установка необходимых утилит
RUN apt-get update && apt-get install -y \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files to the container
COPY . .

# Улучшенный CMD с явным запуском Python
CMD ["python", "-u", "-m", "main"]
