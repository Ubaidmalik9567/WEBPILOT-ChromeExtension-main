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

# FROM python:3.10-slim

# # Install system dependencies for Python packages
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libffi-dev \
#     libjpeg-dev \
#     zlib1g-dev \
#     && apt-get clean


# # Set the working directory to /app/
# WORKDIR /app/

# # Copy the Backend folder to /app/
# COPY Backend/ /app/
# COPY requirements.txt /app/


# # Install Python dependencies
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 5000

# # Command to run your application
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "backend:app"]



