from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Post (BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "welcome to the api"}


@app.get("/posts")
async def get_posts():
    return [
        {"id": 1, "title": "First Post", "content": "Hello World"},
        {"id": 2, "title": "Second Post", "content": "More text"},
    ]


@app.post('/posts')
async def create_post(post: Post):
    return {"data": post}
