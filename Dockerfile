FROM python:3.10-alpine

# Copy the backend files into the container
COPY ./ WEBPILOT-ChromeExtension/backendfile 

# Set the working directory
WORKDIR /WEBPILOT-ChromeExtension/backendfile 

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the backend script
CMD ["python", "backend.py"]

