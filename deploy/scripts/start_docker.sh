#!/bin/bash

aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 730335254649.dkr.ecr.eu-north-1.amazonaws.com
docker pull 730335254649.dkr.ecr.eu-north-1.amazonaws.com/webpilot:latest

# Check if the container 'my-app' is running
if [ "$(docker ps -q -f name=my-app)" ]; then
    # Stop the running container
    docker stop my-app
fi

# Check if the container 'my-app' exists (stopped or running)
if [ "$(docker ps -aq -f name=my-app)" ]; then
    # Remove the container if it exists
    docker rm my-app
fi
docker run -p 5000:5000 --name my-app 730335254649.dkr.ecr.eu-north-1.amazonaws.com/webpilot:latest
echo "Container Start Successfully"