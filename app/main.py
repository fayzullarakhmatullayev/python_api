from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "welcome to the api"}
