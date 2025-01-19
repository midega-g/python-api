import time

import psycopg
from fastapi import Body, FastAPI, Response, HTTPException, status
from pydantic import BaseModel
from psycopg.rows import dict_row

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


def find_post_or_404(post_id):
    """Helper function to find a post by ID or raise a 404 exception."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM posts WHERE id = %s;", (post_id,))
        post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} was not found",
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
        retry_count += 1
        print(f"⚠️ Error: {e}")
        if retry_count < MAX_RETRIES:
            print(f"Retrying in 5 seconds... {retry_count}/{MAX_RETRIES}")
            time.sleep(5)

# This only runs if the loop completes without a successful connection
if retry_count == MAX_RETRIES:
    print("❌ Max retries reached. Could not connect to the database.")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post = Body(...)):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            insert into posts (title, content, published)
            values (%s, %s, %s)
            returning *
            """,
            (post.title, post.content, post.published),
        )
        new_post = cursor.fetchone()
        connection.commit()
    return {"data": new_post}


@app.get("/posts")
def get_posts():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM posts;")
        posts = cursor.fetchall()
        print(posts)
    return {"data": posts}


@app.get("/posts/latest")
def get_latest_posts():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT 5;")
        posts = cursor.fetchall()
        print(posts)
    return {"data": posts}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = find_post_or_404(post_id)
    return {"data": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    find_post_or_404(post_id)
    with connection.cursor() as cursor:
        cursor.execute(
            "delete from posts where id = %s returning *;", (post_id,)
        )
        connection.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post = Body(...)):
    find_post_or_404(post_id)
    post_dict = post.model_dump()
    with connection.cursor() as cursor:
        cursor.execute(
            """
            update posts
            set title = %s, content = %s, published = %s
            where id = %s
            returning *
            """,
            (
                post_dict["title"],
                post_dict["content"],
                post_dict["published"],
                post_id,
            ),
        )
        updated_post = cursor.fetchone()
        connection.commit()
    return {"data": updated_post}
