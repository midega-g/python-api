import time
from typing import Optional

import psycopg
from fastapi import Body, FastAPI, Response, HTTPException, status
from pydantic import BaseModel
from psycopg.rows import dict_row

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "id": 1,
        "title": "Post 1",
        "content": "Content of post 1",
        "published": True,
        "rating": 4,
    },
    {
        "id": 2,
        "title": "Favorite Foods",
        "content": "I like pizza",
        "published": False,
        "rating": 5,
    },
]


def find_post_or_404(post_id: int):
    """Helper function to find a post by ID or raise a 404 exception."""
    post = next((p for p in my_posts if p["id"] == post_id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    return post


MAX_RETRIES = 5
retry_count = 0
while retry_count < MAX_RETRIES:
    try:
        connection = psycopg.connect(
            user="postgres",
            password="password",
            host="localhost",
            port="5432",
            dbname="fastapi",
            row_factory=dict_row,
        )
        print("✅ Connection to PostgreSQL DB successful")
        break
    except psycopg.Error as e:
        print(f"⚠️ Error: {e}")
        retry_count += 1
        print(f"Retrying in 5 seconds... {retry_count}/{MAX_RETRIES}")
        time.sleep(2)

    print("❌ Max retries reached. Could not connect to the database.")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post = Body(...)):
    post_dict = post.model_dump()
    post_dict["id"] = len(my_posts) + 1
    my_posts.append(post_dict)
    return {"data": my_posts}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_posts():
    return {"data": sorted(my_posts, key=lambda p: p["id"], reverse=True)[:2]}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = find_post_or_404(post_id)
    return {"data": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    post = find_post_or_404(post_id)
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post = Body(...)):
    post_dict = post.model_dump()
    post_dict["id"] = post_id
    existing_post = find_post_or_404(post_id)
    existing_post.update(post_dict)
    return {"data": existing_post}
