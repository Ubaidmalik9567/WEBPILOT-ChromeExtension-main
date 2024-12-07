import os
import boto3
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re

# Load AWS credentials from .env file
load_dotenv()

class Scraper:
    def __init__(self):
        self.previous_url = None
        # Initialize S3 client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = os.getenv('AWS_S3_BUCKET_NAME')

    def __write_txt_file(self, text, file_name):
        # Write the text to a file on S3
        line_length = 20
        words = text.split()
        formatted_text = "\n".join([' '.join(words[i:i + line_length]) for i in range(0, len(words), line_length)])
        
        # Upload to S3 instead of writing to local file system
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=file_name,
            Body=formatted_text
        )
        print(f"Data saved to S3 as {file_name}")

    def is_new_url(self, new_url):
        if self.previous_url is not None and self.previous_url == new_url:
            return False
        else:
            self.previous_url = new_url
            return True

    def scrape_website(self, url):
        if self.is_new_url(new_url=url):
            pass
        else:
            pass

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return response.status_code

        soup = BeautifulSoup(response.text, 'html.parser')

        def extract_text(elements):
            return [element.get_text(separator=" ").strip() for element in elements if element.get_text().strip()]

        headings = extract_text(soup.find_all('h1'))
        paragraphs = extract_text(soup.find_all('p'))
        list_items = extract_text(soup.find_all('li'))
        articles = extract_text(soup.find_all('article'))
        sections = extract_text(soup.find_all('section'))
        block_quote = extract_text(soup.find_all('blockquote'))
        tables = extract_text(soup.find_all('tr'))

        all_text = headings + paragraphs + articles + block_quote + sections + tables + list_items
        result_string = ' '.join(all_text)

        formatted_text = re.sub(r'\s+', ' ', result_string)

        # Use the S3 path instead of local path
        file_name = "scraped_data.txt"
        self.__write_txt_file(text=formatted_text, file_name=file_name)

        return response.status_code

    def Tab_data(self, text):
        print("Data Scrapping function called...")
        # Instead of saving locally, save to S3
        file_name = "scraped_data.txt"
        self.__write_txt_file(text=text, file_name=file_name)
        print("Text data saved successfully.")
