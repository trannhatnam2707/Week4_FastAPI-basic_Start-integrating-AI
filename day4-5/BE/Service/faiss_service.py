import faiss
import numpy as np
import os

FAISS_INDEX_FILE = "vector_store.index"

def load_faiss_index(dimension: int):
    """
    Load FAISS index nếu tồn tại, nếu chưa có thì tạo mới 
    """
    if os.path.exists(FAISS_INDEX_FILE): 
       index = faiss.read_index(FAISS_INDEX_FILE) 
       print("FAISS index loaded from file") 
    else: # Tạo IndexFlatL2 bình thường 
       flat_index = faiss.IndexFlatL2(dimension)
       # Gói thêm IDMap để có thể lưu ID tùy chỉnh
       index = faiss.IndexIDMap(flat_index) 
       print("New FAISS index with IDMap created")
    return index

def save_faiss_index(index):
    """ Lưu FAISS index ra file. """
    faiss.write_index(index, FAISS_INDEX_FILE)
    print("FAISS index saved to file")

def add_embeddings_to_faiss(embeddings: list[list[float]], ids: list[int]):
    """
    Thêm embeddings với ID tùy chỉnh và lưu lại 
    embeddings: list vector float 
    ids: list int, ID tương ứng để map với DB
    """
    if not embeddings or not ids or len(embeddings) != len(ids):
        raise ValueError("Embeddings và IDs phải cùng độ dài và không rỗng")
    
    
    embeddings_np = np.array(embeddings, dtype='float32')
    ids_np = np.array(ids, dtype='int64')  # FAISS yêu cầu int64
    
    
    #load index 
    index = load_faiss_index(dimension=embeddings_np.shape[1])
    
    #thêm vector kèm ID
    index.add_with_ids(embeddings_np, ids_np)
    #lưu index
    save_faiss_index(index)
    print(f"Added {len(embeddings)} vectors to FAISS with IDs")
#ok
