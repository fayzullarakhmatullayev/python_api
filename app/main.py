from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post (BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="pythonapi",
#                                 user="postgres", password="admin", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was succesfull')
#         break
#     except Exception as error:
#         print("conection to database was failed")
#         print("Error: ", error)
#         time.sleep(2)


@app.get("/")
async def root():
    return {"message": "welcome to the api"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get('/posts/{id}')
async def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * from posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return {"post_detail": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
async def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #                (post.title, post.content, post.published, str(id),))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post.first()}
