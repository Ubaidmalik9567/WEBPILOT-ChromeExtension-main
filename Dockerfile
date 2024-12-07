FROM python:3.10-slim

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app/
WORKDIR /app/

# Copy the Backend folder and requirements.txt to /app/
COPY Backend/ /app/
COPY requirements.txt /app/
COPY .env /app/.env

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set environment variables for Flask
ENV FLASK_APP=backend.py
ENV FLASK_ENV=development

# Expose the application port
EXPOSE 5000

# Command to run your Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
