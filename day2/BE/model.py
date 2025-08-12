from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    author: str      
    
    #Route update_post
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None