FROM python:3.10-alpine

# Install dependencies for building Python packages
RUN apk add --no-cache gcc musl-dev g++ libffi-dev jpeg-dev zlib-dev

# Copy files into the container
COPY ./ WEBPILOT-ChromeExtension/backendfile

# Set the working directory
WORKDIR /WEBPILOT-ChromeExtension/backendfile

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Command to run your application
CMD ["python", "backend.py"]
