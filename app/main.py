from fastapi import FastAPI

from .models import Base
from .routers import post, user
from .database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
