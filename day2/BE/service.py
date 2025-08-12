from unittest import result
from bson.objectid import ObjectId
from database import post_collection
from model import Post, PostUpdate



# Chuyển document MongoDB thành dict trả về JSON (đổi _id -> id dạng chuỗi)
def serialize_post(post):
    return {
        "id": str(post["_id"]),   # Chuyển ObjectId -> string
        "title": post["title"],
        "content": post["content"],
        "author": post["author"]
    }
    
#get all post
def get_all_post():
    posts = list(post_collection.find())
    return [serialize_post(post) for post in posts ]

#get post by id
def get_post_by_id(id: str):
    post = post_collection.find_one({"_id":ObjectId(id)})
    if post:
        return serialize_post(post)
    else:
        return {"message":"Không tìm thấy bài viết"}
    
#Create post
def create_post(post: Post):
    # Chuyển Post model thành dict thuần để MongoDB lưu  
    result = post_collection.insert_one(post.model_dump())
    #  # Tìm document vừa insert bằng _id mới tạo để lấy toàn bộ dữ liệu
    new_post = post_collection.find_one({"_id": result.inserted_id})
    return serialize_post(new_post)

#Delete Post by id
def delete_post_by_id(id:str):
    result = post_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0

#update Post
def update_post_by_id(id:str, update_post: PostUpdate):
    #chuyển đổi sang dạng dictionary và lấy từng cặp key, value ra
    update_data = {key: value for key, value in update_post.model_dump().items() if value is not None}
    if not update_data:
        return None
    post_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    updated_post = post_collection.find_one({"_id": ObjectId(id)})
    return serialize_post(updated_post) if updated_post else None