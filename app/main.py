from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post (BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="pythonapi",
                                user="postgres", password="admin", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was succesfull')
        break
    except Exception as error:
        print("conection to database was failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "welcome to the api"}


@app.get("/posts")
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get('/posts/{id}')
async def get_post(id: int):
    cursor.execute("SELECT * from posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return {"post_detail": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
async def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, str(id),))

    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return {"data": updated_post}
