from pydantic import BaseModel
from fastapi import FastAPI, Query

app = FastAPI()
 
# Giả lập "database"
users = []
next_id = 1

class User(BaseModel):
    name: str
    age: int
    address: str 

# Route get all users
@app.get("/users")
def getAllUsers():
    return {"users": users}

# Route get user by id (path parameter)
@app.get("/users/{id}")
def getUserById(id: int):
    for user in users:
        if user["id"] == id:
            return {"user": user}
    return {"error": "User không tồn tại"}

# Route get user by name (query parameter)
@app.get("/users/search")
def getUserByName(name: str = Query(description="Tên user cần tìm")):
    for user in users:
        if user["name"].lower() == name.lower():
            return {"user": user}
    return {"error": "User không tồn tại"}

# Route Post user   
@app.post("/users")
def create_user(user: User):
    global next_id
    new_user = {
        "id": next_id,
        "name": user.name,
        "age": user.age,
        "address": user.address
    }
    users.append(new_user)
    next_id += 1
    return {"message": "User created", "user": new_user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
