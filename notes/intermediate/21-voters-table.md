
# Implementing a Voting/Like System in a Social Media App

## Overview

- Social media apps often include a voting or likes system (e.g., Facebook likes, Reddit upvotes/downvotes, Instagram/Twitter likes).
- This system allows users to like posts, ensures users can only like a post once, and retrieves the total number of likes for a post.

## Requirements for the Voting System

1. **User Actions**:
   - A user should be able to like a post.
   - A user should only be able to like a post **once** (no duplicate likes).
   - When retrieving a post, the total number of likes should also be fetched.

2. **Database Design**:
   - A separate table (`votes`) is needed to store likes.
   - The table should have:
     - `post_id`: References the post being liked.
     - `user_id`: References the user who liked the post.
   - For upvote/downvote systems (e.g., Reddit), a third column for vote direction could be added, but this example focuses on a simple like system.

## Key Concepts

### Composite Keys

- A **composite key** is a primary key that spans multiple columns.
- Ensures that the combination of `post_id` and `user_id` is unique.
- Prevents a user from liking the same post more than once.

#### Example of Composite Key in Action

| `post_id` | `user_id` |
|-----------|-----------|
| 12        | 4         |
| 28        | 9         |
| 12        | 9         |
| 55        | 2         |

- Valid: User 4 likes Post 12, User 9 likes Post 12, User 9 likes Post 28.
- Invalid: User 2 likes Post 55 **twice** (duplicate combination).

## Creating the `votes` Table in PostgreSQL (pgAdmin)

### Steps

1. **Create Table**:
   - Table Name: `votes`
   - Columns:
     - `post_id` (integer, primary key)
     - `user_id` (integer, primary key)

2. **Set Up Foreign Keys**:
   - `post_id` references `posts(id)` with `ON DELETE CASCADE`.
   - `user_id` references `users(id)` with `ON DELETE CASCADE`.

3. **Composite Primary Key**:
   - Combine `post_id` and `user_id` to ensure uniqueness.

### Example SQL Commands

```sql
CREATE TABLE votes (
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, user_id)
);
```

## Implementing the Votes Table in SQLAlchemy

1. Open `models.py` and define the **Vote model**:

    ```python
    class Vote(Base):
        __tablename__ = "votes"

        user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
        post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    ```

2. Explanation:
   - The table name is `votes`.
   - `user_id` and `post_id` are **foreign keys** and **primary keys**, forming a composite key.
   - `ondelete="CASCADE"` ensures that if a user or post is deleted, their associated votes are also removed.
3. Save the file and restart the application.
4. Verify the table creation in **pgAdmin**:
   - Check columns, primary keys, and constraints.
   - Ensure cascade deletion is properly set up.

## Testing the `votes` Table

### Inserting Data

- Insert a valid like:

  ```sql
  INSERT INTO votes (post_id, user_id) VALUES (10, 21);
  ```

- Attempt to insert a duplicate like:

  ```sql
  INSERT INTO votes (post_id, user_id) VALUES (10, 21); -- Error: Duplicate entry
  ```

- Attempt to insert a like with invalid `post_id` or `user_id`:

  ```sql
  INSERT INTO votes (post_id, user_id) VALUES (99, 21); -- Error: Invalid post_id
  INSERT INTO votes (post_id, user_id) VALUES (10, 99); -- Error: Invalid user_id
  ```

[[TOC]]
