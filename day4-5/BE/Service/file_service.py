#đọc và tạo chunk từ file bất kỳ
from pathlib import Path
from PyPDF2 import PdfReader
import docx

def read_file_content_from_path(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    text = ""


#Đọc toàn bộ file .txt và gán vào text.
    if ext == ".txt": 
        with open(file_path, "r", encoding="utf-8") as f: 
            text = f.read()
            
#Đọc từng trang, lấy text, nối (+=) vào biến text.
    elif ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n" #extract_text() lấy nội dung chữ
            
#Lấy text từ từng đoạn trong Word, ghép lại thành một chuỗi.
    elif ext == ".docx":
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        
    else:
        raise ValueError(f"Không hỗ trợ định dạng file: {ext}")
    return text     

def chunk_text(text: str, chunk_size=100, overlap=20) -> list:
    words = text.split()
    chunks = []
    start = 0 
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks
#oke