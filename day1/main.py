from pydantic import BaseModel
from fastapi import FastAPI, Query
import json
import os

app = FastAPI()

# File JSON để lưu users
USERS_FILE = "users.json"

# Hàm đọc users từ file JSON
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Hàm lưu users vào file JSON
def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# Hàm lấy ID tiếp theo
def get_next_id(users):
    if not users:
        return 1
    return max(user["id"] for user in users) + 1

class User(BaseModel):
    name: str
    age: int
    address: str 

# Route get all users
@app.get("/")
def getAllUsers():
    users = load_users()
    return {"users": users}

# Route get user by name (query parameter)
@app.get("/users/search")
def getUserByName(name: str = Query(default="", description="Tên người dùng cần tìm")):
    users = load_users()
    
    if not name:
        return {"message": "Vui lòng nhập tên để tìm kiếm"}
    
    matched_users = [user for user in users if name.lower() in user["name"].lower()]
    
    if matched_users:
        return {"results": matched_users}
    return {"message": "Không tìm thấy user nào", "searched_name": name}

# Route get user by id (path parameter)
@app.get("/users/{id}")
def getUserById(id: int):
    users = load_users()
    for user in users:
        if user["id"] == id:
            return {"user": user}
    return {"error": "User không tồn tại"}

# Route Post user   
@app.post("/users")
def create_user(user: User):
    users = load_users()
    new_id = get_next_id(users)
    
    new_user = {
        "id": new_id,
        "name": user.name,
        "age": user.age,
        "address": user.address
    }
    
    users.append(new_user)
    save_users(users)
    
    return {"message": "User created successfully", "user": new_user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
