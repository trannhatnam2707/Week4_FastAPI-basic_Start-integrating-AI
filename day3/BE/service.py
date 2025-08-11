from urllib import response
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key= os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


#chọn model GEMINI
model = genai.GenerativeModel("gemini-1.5-flash")
def get_ai_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Lỗi: {str(e)}"