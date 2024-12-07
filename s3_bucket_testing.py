import os
import boto3
from dotenv import load_dotenv

# Load AWS credentials from .env file
load_dotenv()

def get_file_from_s3(file_name):
    try:
        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
        
        # Fetch the file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        file_content = response['Body'].read().decode('utf-8')
        print("File content successfully retrieved:")
        print(file_content)
        return file_content
    except Exception as e:
        print(f"Error retrieving file: {e}")
        return None

# Call the function to retrieve the file
get_file_from_s3("scraped_data.txt")