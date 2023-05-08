from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random


app = FastAPI()


class Post (BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "title": "First Post",
        "content": "Hello World",
        "published": True,
        "rating": None,
        "id": 1
    },
    {
        "title": "Second Post",
        "content": "More text",
        "published": True,
        "rating": None,
        "id": 2
    },
    {
        "title": "Third Post",
        "content": "Even more text",
        "published": True,
        "rating": None,
        "id": 3
    },
]


@app.get("/")
async def root():
    return {"message": "welcome to the api"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post('/posts')
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = random.randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get('/posts/{id}')
async def get_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return {"data": post}
    return {"data": "post not found"}
