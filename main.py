from fastapi import FastAPI, Response, status, HTTPException
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


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = random.randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get('/posts/{id}')
async def get_post(id: int, response: Response):
    for post in my_posts:
        if post['id'] == id:
            response.status_code = status.HTTP_200_OK
            return {"data": post}
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id {id} not found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")


@app.delete('/posts/{id}')
async def delete_post(id: int, response: Response):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            my_posts.pop(index)
            response.status_code = status.HTTP_204_NO_CONTENT
            return {"data": f"post with id {id} deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")
