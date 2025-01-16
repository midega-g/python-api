from typing import Optional

from fastapi import Body, FastAPI, Response, HTTPException, status
from pydantic import BaseModel, PositiveInt

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[PositiveInt] = None


def find_post_or_404(post_id: int):
    """Helper function to find a post by ID or raise a 404 exception."""
    post = next((p for p in my_posts if p["id"] == post_id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    return post


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
