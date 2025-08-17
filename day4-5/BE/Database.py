from pymongo import MongoClient
from datetime import datetime 
import numpy as np

MONGO_URL = "mongodb://localhost:27017" 
client = MongoClient(MONGO_URL)
db = client["RAG_DB"] 
embedding_collection = db["embeddings"]


def save_embeddings_to_mongo(file_name: str, chunks: list[str], ids: list[int], source: str = None):
    docs = []
    for content, faiss_id in zip(chunks, ids):
        doc = {
            "fileName": file_name,
            "content": content,
            "faiss_id": faiss_id,
            "meta": {
                "source": source if source else "",
                "uploadedAt": datetime.utcnow()
            }
        }
        docs.append(doc)

    if docs:
        embedding_collection.insert_many(docs)

                