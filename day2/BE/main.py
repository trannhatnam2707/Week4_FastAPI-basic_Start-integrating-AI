from types import new_class
from typing import Optional
from fastapi import FastAPI, Query
import json
from pydantic import BaseModel
from starlette.responses import Content
from cors_config import configure_cors


app = FastAPI()

# Cấu hình CORS từ file riêng
configure_cors(app)

POSTS_FILE = "posts.json"

#Đọc file posts.json
def read_posts():
    with open(POSTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

#Lưu file posts.json
def save_posts(posts):
    with open(POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

#Lấy id bài post tiếp theo
def get_next_id(posts):
    if not posts:
        return 1
    return max(post["id"] for post in posts) + 1

class Post(BaseModel):
    title: str
    content: str
    author: str                                         

#Route get all posts
@app.get("/")
def get_all_posts():
    posts = read_posts()
    return {"posts": posts}

#Route get post by title
@app.get("/posts/search_by_title")
def get_post_by_title(title: str = Query(default="", description="Tên bài post cần tìm")):
    posts = read_posts()
    if not title:
        return {"message": "Vui lòng nhập tên bài post để tìm kiếm"}
    matched_posts = [post for post in posts if title.lower() in post["title"].lower()]
    if matched_posts:
        return {"results": matched_posts}
    return {"message": "Không tìm thấy bài post nào", "searched_title": title}

#Route get post by content
@app.get("/posts/search_by_content")
def get_post_by_content(content: str = Query(default="", description="Nội dung bài post cần tìm")):
    posts = read_posts()
    if not content:
        return {"message": "Vui lòng nhập nội dung bài post để tìm kiếm"}
    matched_posts = [post for post in posts if content.lower() in post["content"].lower()]
    if matched_posts:
        return {"results": matched_posts}
    return {"message": "Không tìm thấy bài post nào", "searched_content": content}

#Route get post by author
@app.get("/posts/search_by_author")
def get_post_by_author(author: str = Query(default="", description="Tác giả bài post cần tìm")):
    posts = read_posts()
    if not author:
        return {"message": "VUi lòng nhập tên tác giả vào dây"}
    matched_posts = [post for post in posts if author.lower() in post[author].lower()]
    if matched_posts:
        return {"message": matched_posts}
    return {"message":"Không tìm thấy tác giả này", "search_author": author}

#Route get post by id
def get_post_by_id(id: int):
    posts = read_posts()
    for post in posts:
        if post["id"] == id:
            return {"post": post}
    return {"error": "Bài post không tồn tại"}

@app.get("/posts/{id}")
def get_post_by_id_route(id: int):
    return get_post_by_id(id)

#Route Post bài Post
@app.post("/posts") 
def create_post(post: Post):
    posts = read_posts()
    new_id = get_next_id(posts)

    new_post = {
    "id": new_id,
    "title": post.title,
    "content": post.content,
    "author": post.author
}
    posts.append(new_post)
    save_posts(posts)
    return {"message": "Post created successfully", "Post": new_post}

#Route Delete-all post 
@app.delete("/post")
def delete_all_posts():
    save_posts([])
    return {"message":"Đã xóa toàn bộ bài post"}

#Route delete post
@app.delete("/posts/{id}")
def delete_post_by_id(id: int):
    posts = read_posts()
    new_posts= [post for post in posts if post["id"] != id ]
    if len(new_posts) == len(posts):
        return {"message":"Không tìm thấy bài post để xóa"}
    save_posts(new_posts)
    return {"message": f"Đã xóa bài post id {id}"}

#Route update_post
class PostUpdate(BaseModel):
    title: Optional[str] = None
    Content: Optional[str] = None
    author: Optional[str] = None

@app.put("/posts/{id}")
def update_post(id: int, update_post:PostUpdate):
    posts= read_posts()
    for post in posts:
        if post["id"] == id:
            if update_post.title is not None:
                post["title"] = update_post.title
            if update_post.content is not None:
                post["content"] = update_post.content
            if update_post.author is not None:
                post["author"] = update_post.author
            save_posts(posts)
            return {"message": f"Đã cập nhật post id {id}", "post": post}
        return {"error": "Không tìm thấy bài post để cập nhật"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



