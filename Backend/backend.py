from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from RAG_QnA import RAG_Model
from scrap import Scraper
import requests
import re
from urllib.parse import urlparse, unquote

app = FastAPI()

# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Utility functions to validate URLs
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def get_file_url(file_url):
    if file_url.startswith("https://"):
        return file_url
    else:
        parsed_url = urlparse(file_url)
        file_path = parsed_url.path
        file_path = unquote(file_path)
        return file_path

def is_pdf_url(url):
    if url.lower().endswith('.pdf'):
        return True
    try:
        response = requests.head(
            url=url, 
            allow_redirects=True
        )
        content_type = response.headers.get('Content-Type', '')
        is_doc = content_type.lower() == 'application/pdf'
        print("Is PDF: ", is_doc)
        return is_doc

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False

def is_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+',
        re.IGNORECASE
    )
    return re.match(youtube_regex, url) is not None

# Initialize models
scrp = Scraper()
rag = RAG_Model()

# Request models
class ProcessPageRequest(BaseModel):
    url: str
    text: str

class GenerateResponseRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Welcome"}

@app.post("/process_page")
async def process_page(request: ProcessPageRequest):
    try:
        url = request.url
        text = request.text
        
        if not url:
            raise HTTPException(status_code=400, detail="Missing URL")
        
        if not text:
            raise HTTPException(status_code=400, detail="Missing text")
        
        print(f"URL: {url}")

        if is_pdf_url(url):
            parse_url = get_file_url(file_url=url)
            print("Parse URL: ", parse_url)
            rag.load_Database(is_pdf=True, pdf_url=parse_url)
        elif is_youtube_url(url):
            print("URL Type: Youtube Video")
            rag.load_Database(is_youtube_url=True, youtube_url=url)
        else:
            print("This is Website URL")
            scrp.Tab_data(text=text)
            rag.load_Database()

        return JSONResponse(content={"message": "Page processed successfully"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_response")
async def generate_response(request: GenerateResponseRequest):
    try:
        user_input = request.message

        if not user_input:
            raise HTTPException(status_code=400, detail="Missing message")

        response = rag.generateResponse(user_input)
        print(response)
        
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))