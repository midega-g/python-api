# Implementing Foreign Key

## Current Application Setup

- **Database Structure**:
  - Two tables: `users` and `posts`.
  - **Users Table**: Allows creating, modifying, and deleting users.
  - **Posts Table**: Allows creating, modifying, and deleting posts.
- **Problem**:
  - Posts are not associated with the users who created them.
  - In a typical application (e.g., social media), each post should display the user who created it.

## Relational Databases and Relationships

- **Core Concept**:
  - Relational databases allow tables to be connected through relationships.
  - In this case, we need to link the `posts` table to the `users` table.

### Setting Up a Relationship

#### Step 1: Add a Foreign Key Column

- **New Column**:
  - Add a column in the `posts` table called `user_id`.
  - Purpose: Store the ID of the user who created the post.
- **Foreign Key**:
  - A foreign key is a column that links to another table.
  - Specifies:
    1. The table to connect to (`users` table).
    2. The column to reference (`id` column in the `users` table).

!!! note Example

- **Post Table**:
  - Columns: `id`, `title`, `content`, `published`, `created_at`, `user_id`.
  - `user_id` stores the ID of the user who created the post.
- **Users Table**:
  - Columns: `id`, `name`, `email`, etc.
  - Example: A post with `user_id = 212` was created by the user with `id = 212`.

### One-to-Many Relationship

- **Definition**:
  - One user can create many posts.
  - Each post is associated with only one user.
- **Why It’s Called "One-to-Many"**:
  - One user → Many posts.
  - A post cannot belong to multiple users.

### More about Foreign Keys

- **Foreign Key Flexibility**:
  - Foreign keys do not always have to point to the `id` column of another table.
  - They can reference other columns, depending on the application's requirements.
- **Example**:
  - If needed, a foreign key could reference an `email` column instead of `id`.

## Manual Implementation in PostgreSQL

### Preparing the Database

- **Delete Existing Data**:
  - To simplify the process of adding a new column and foreign key, delete all rows from the `posts` table using the command below in pgAdmin:

    ```sql
    DELETE FROM posts;
    ```

  - **Reason**: Adding a `NOT NULL` column to a table with existing rows requires additional steps (e.g., providing default values) thus, deleting rows avoids this complexity.

### Adding the `user_id` Column

1. **Open PGAdmin**:
   - Right-click on the `posts` table and select **Properties**.
2. **Add a New Column**:
   - Go to the **Columns** tab and add a new column named `user_id`.
   - **Naming**: Use a descriptive name like `user_id` to indicate the relationship.
3. **Data Type**:
   - Match the data type of `user_id` to the `id` column in the `users` table.
     - Example: If `id` in `users` is `integer`, set `user_id` to `integer`.
     - If `id` is `UUID`, set `user_id` to `UUID`.
4. **NOT NULL Constraint**:
   - Decide whether `user_id` should allow `NULL` values.
     - If posts must always be associated with a user, set `NOT NULL`.
     - Example:

       ```sql
       user_id INTEGER NOT NULL
       ```

### Setting Up the Foreign Key

1. **Go to Constraints**:
   - In the `posts` table properties, navigate to the **Constraints** tab.
2. **Add Foreign Key**:
   - Click the **+** button to add a new foreign key.
   - **Naming Convention**:
     - The naming convention is usually, `table1_table2_fkey` and should be descriptive which in this case would be `posts_users_fkey`.
3. **Configure the Foreign Key**:
   - **Local Column**: Select `user_id` (the column in the `posts` table).
   - **Referenced Table**: Select the `users` table.
   - **Referenced Column**: Select the `id` column in the `users` table.
4. **Actions**:
   - **On Delete**: Choose what happens when a user is deleted.
     - **Cascade**: Automatically delete posts created by the deleted user.
     - **Set Null**: Set `user_id` to `NULL` for posts created by the deleted user (requires `user_id` to allow `NULL`).
     - **Set Default**: Assign a default value to `user_id` for posts created by the deleted user.
   - **On Update**: Choose what happens when a user's `id` is updated (usually left as `NO ACTION`).

### Testing the Foreign Key

1. **Insert Data**:
   - Add a new post with a valid `user_id` (e.g., `17`).
     - Example:

       ```sql
       INSERT INTO posts (title, content, user_id) VALUES ('My First Post', 'Some content', 17);
       ```

   - **Error Handling**:
     - If `user_id` is `NULL` or references a non-existent user, PostgreSQL will throw an error.
     - Example: `null value in column "user_id" violates not-null constraint` or `foreign key constraint violation`.

2. **Query Data**:
   - Retrieve all posts created by a specific user.
     - Example:

       ```sql
       SELECT * FROM posts WHERE user_id = 17;
       ```

3. **Delete User**:
   - Delete a user and observe the effect on related posts.
     - Example:

       ```sql
       DELETE FROM users WHERE id = 17;
       ```

   - If `ON DELETE CASCADE` is set, all posts created by the deleted user will also be deleted.

### Cleaning Up

- **Remove the `user_id` Column**:
  - Since we'll be using SQLAlchemy to automate the creation of foreign keys and relationships in your application, we will have to delete the `user_id` column and its foreign key constraint.
  - Steps:
    1. Delete the foreign key constraint from the **Constraints** tab.
    2. Delete the `user_id` column from the **Columns** tab.
  - **Note**: Ensure no data dependencies exist before deleting.

## Implementation Using SQLAlchemy

### Overview

- **Goal**: Use SQLAlchemy to create and manage foreign keys in the database.
- **Why**: Automate table creation and foreign key constraints instead of manually setting them up in PostgreSQL.

### Steps to Add a Foreign Key in SQLAlchemy

#### 1. Update the `Post` Model

- **Add a New Column**:
  - In `models.py`, add a column to the `Post` class to represent the foreign key.

    ```python
    class Posts:
      # other code logic goes here
      owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    ```

  - **Details**:
    - `owner_id`: Name of the column (can be `user_id` or any descriptive name).
    - `Integer`: Data type must match the `id` column in the `users` table.
    - `ForeignKey('users.id')`: Specifies the foreign key relationship to the `id` column in the `users` table.
    - `nullable=False`: Ensures the column cannot be `NULL`.

#### 2. Set Up `ON DELETE` Behavior

- **Cascade Deletion**:
  - Automatically delete posts when the associated user is deleted.

  - **Options**:
    - `CASCADE`: Delete child rows when the parent row is deleted.
    - `SET NULL`: Set the foreign key to `NULL` (requires `nullable=True`).
    - `SET DEFAULT`: Set the foreign key to a default value.

### Testing the Implementation

#### 1. Restart the Application

- SQLAlchemy will create the `posts` table with the new `owner_id` column and foreign key constraint.
- **Note**: If the table already exists, SQLAlchemy will not update it. You must either:
  - Manually update the table in PostgreSQL.
  - Drop the table and let SQLAlchemy recreate it (recommended for development).

#### 2. Verify the Table Structure

- **Check in PGAdmin**:
  - Refresh the database and inspect the `posts` table.
  - Confirm:
    - The `owner_id` column exists and is set to `NOT NULL`.
    - The foreign key constraint is correctly configured with `ON DELETE CASCADE`.

#### 3. Insert Data

- **Create Posts**:
  - Insert posts with valid `owner_id` values (must match existing user IDs).

    ```sql
    INSERT INTO posts (title, content, owner_id) VALUES ('Post One', 'Some content', 20);
    ```

  - **Error Handling**:
    - Attempting to insert a post with an invalid `owner_id` (e.g., `57`) will throw a foreign key constraint error.
    - Attempting to insert a post with `NULL` `owner_id` will throw a `NOT NULL` constraint error.

#### 4. Test Cascade Deletion

- **Delete a User**:
  - Delete a user and verify that all associated posts are automatically deleted.

    ```sql
    DELETE FROM users WHERE id = 20;
    ```

  - **Result**:
    - Posts with `owner_id = 20` will be deleted.

### Common Issues and Fixes

#### 1. Table Already Exists

- **Problem**: SQLAlchemy does not update existing tables.
- **Solution**:
  - Drop the table and let SQLAlchemy recreate it (for development).
  - Use a database migration tool (e.g., Alembic) for production.

#### 2. Schema Mismatch

- **Problem**: Hardcoded schemas in the application may not match the updated database structure.
- **Solution**:
  - Update the application schema to include the new `owner_id` field.

[[TOC]]
