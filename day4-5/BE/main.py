import os
import tempfile
import uuid
from fastapi import FastAPI, UploadFile
from Service.file_service import chunk_text, read_file_content_from_path
from Service.embedding_service import create_embedding
from Service.faiss_service import add_embeddings_to_faiss

from Database import save_embeddings_to_mongo
# from Service.faiss_service import add_embeddings_to_faiss


from cosr_config import configure_cors

app = FastAPI(title="RAG file upload API")
configure_cors(app)

@app.post("/upload")
async def process_files(files: list[UploadFile]):
    result = []
    for file in files:
        # Lấy phần mở rộng của file gốc (.txt, .pdf, .docx)
        _, ext = os.path.splitext(file.filename)
        
        # Tạo file tạm và giữ nguyên phần mở rộng
        temp_path = tempfile.mktemp(suffix=ext)
        
        # ghi nội dung vào file tạm
        with open(temp_path, "wb") as f:
            f.write(await file.read())

       
        text = read_file_content_from_path(temp_path)

        # Chia chunk
        chunks = chunk_text(text, chunk_size=100, overlap=20)
        print(f"Tổng số chunk: {len(chunks)}")
        
        # Tạo embedding
        embeddings = [create_embedding(chunk) for chunk in chunks]

        #lưu vào faiss
        # ids = [str(uuid.uuid4()) for _ in chunks] #mỗi chunk một id duy nhất
        ids = list(range(len(chunks)))  # hoặc lấy offset từ FAISS index size
        add_embeddings_to_faiss(embeddings, ids)

        # # Lưu vào MongoDB
        save_embeddings_to_mongo(file.filename, chunks, ids)

        result.append({
            "file": file.filename,
            "chunks": len(chunks),
            "faiss_ids": ids
        })

        
    
    return {"processed_files": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


#ok