# llama_integration.py
import requests
import os
from dotenv import load_dotenv


load_dotenv()

llama_api_url = os.getenv("LLAMA_API_URL")

def generate_response(query: str, context: str):
    response = requests.post(llama_api_url, json={"query": query, "context": context})
    return response.json().get("response", "Không thể tạo phản hồi")