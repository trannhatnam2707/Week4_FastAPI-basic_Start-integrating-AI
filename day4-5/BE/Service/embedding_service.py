import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

#lấy API key từ biến môi trường
genai.configure(api_key=os.getenv("Gemini_api_key"))

def create_embedding(text: str) -> list:
    # Tạo embedding vector từ 1 đoạn text
    if not text.strip():
        return []
        
    response = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    
    return response["embedding"]
#ok 