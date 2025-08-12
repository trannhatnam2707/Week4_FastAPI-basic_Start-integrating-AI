from pymongo import  MongoClient
MONGO_URL="mongodb://localhost:27017"

client =  MongoClient(MONGO_URL)

db=client["post_article"] #tên DB
post_collection = db["posts"] #tên collection
