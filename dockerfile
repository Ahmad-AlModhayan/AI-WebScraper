# Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG ar_SA.UTF-8
ENV LANGUAGE ar_SA
ENV LC_ALL ar_SA.UTF-8
ENV PYTHONPATH=/app

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for multilingual support
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Generate locales
RUN sed -i '/ar_SA.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen ar_SA.UTF-8

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional ML dependencies
RUN pip install \
    torch \
    transformers \
    sentence-transformers \
    ollama

# Expose the port the app runs on
EXPOSE 8501

# Create necessary directories
RUN mkdir -p logs data/cache data/exports

# Set the default command to run the application
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
