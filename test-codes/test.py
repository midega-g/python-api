if __name__ == "__main__":

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

    post_id = 2
    print(next((p for p in my_posts if p["id"] == post_id), None))
