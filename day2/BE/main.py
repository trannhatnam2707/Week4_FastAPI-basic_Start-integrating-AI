from fastapi import FastAPI
from cors_config import configure_cors
from model import Post, PostUpdate
from service import create_post, delete_post_by_id, get_all_post, get_post_by_id, update_post_by_id


app = FastAPI()
# Cấu hình CORS từ file riêng
configure_cors(app)
                                
#Route get all posts
@app.get("/posts")
def get_all_posts():
    return {"posts":get_all_post()}

#Route get post by id
@app.get("/posts/{id}")
def get_post_id(id: str):
    post = get_post_by_id(id)
    if post:
        return {"post" : post}
    return {"error": "Bài post này không tồn tại"}


#Route Post bài Post
@app.post("/posts") 
def create(post: Post):
    new_post = create_post(post)
    return {"message": "Đăng bài thành công", "post": new_post}

#Route delete post
@app.delete("/posts/{id}")
def delete(id: str):
    if delete_post_by_id(id):
        return {"message": f"Đã xóa bài post id {id}"}
    return {"message": "Không tìm thấy bài post để xóa"}

#Route update_post
@app.put("/posts/{id}")
def update(id: str, update_post: PostUpdate):
    updated = update_post_by_id(id, update_post)
    if updated: 
        return {"message": f"Đã cập nhật post {id}","post": updated}
    return {"error": "Không tìm thấy bài post để update"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



