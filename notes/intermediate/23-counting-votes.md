# SQL Joins and Advanced Queries

## Overview

In this section, we will go about how to use SQL joins to retrieve data from multiple tables, specifically focusing on the `Posts` and `Votes` tables. That way, we will also cover grouping and counting data to get meaningful insights, such as the number of votes per post.

## Why Use Joins?

- **Single Query Efficiency**: Instead of querying multiple tables separately, joins allow us to retrieve data from multiple tables in a single query.
- **Relationships**: Tables often have relationships (e.g., a `post` is created by a `user`). Joins help combine related data for better analysis and display.

## Types of Joins

1. **Left Join**: Retrieves all records from the left table and matching records from the right table. If no match is found, `NULL` is returned for the right table.
2. **Right Join**: Retrieves all records from the right table and matching records from the left table. If no match is found, `NULL` is returned for the left table.
3. **Inner Join**: Retrieves only records that have matching values in both tables.
4. **Outer Join**: Retrieves all records when there is a match in either the left or right table.

## Example: Joining `Posts` and `Users`

To display posts along with the username or email of the user who created them, we use a **left join**.

**Query:**

```sql
SELECT posts.*, users.email
FROM posts
LEFT JOIN users
ON posts.owner_id = users.id;
```

**Explanation:**

- `posts.*`: Retrieves all columns from the `posts` table.
- `users.email`: Retrieves the `email` column from the `users` table.
- `LEFT JOIN`: Combines rows from `posts` and `users` where `posts.owner_id` matches `users.id`.
- If a post has no matching user, the `email` field will be `NULL`.

## Handling Ambiguous Column Names

When joining tables, columns with the same name (e.g., `id`) can cause ambiguity. To resolve this, prefix the column name with the table name.

**Query:**

```sql
SELECT posts.id, users.email
FROM posts
LEFT JOIN users
ON posts.owner_id = users.id;
```

**Explanation:**

- `posts.id`: Specifies the `id` column from the `posts` table.
- `users.email`: Specifies the `email` column from the `users` table.

## Counting Posts per User

To count the number of posts created by each user, use a **group by** clause.

**Query:**

```sql
SELECT users.id, users.email, COUNT(posts.id) AS post_count
FROM users
LEFT JOIN posts
ON users.id = posts.owner_id
GROUP BY users.id;
```

**Explanation:**

- `COUNT(posts.id)`: Counts the number of posts for each user.
- `GROUP BY users.id`: Groups the results by user ID.
- If a user has no posts, `post_count` will be `0`.

## Joining `Posts` and `Votes`

To retrieve posts along with their vote counts, use a **left join** and **group by**.

**Query:**

```sql
SELECT posts.*, COUNT(votes.post_id) AS vote_count
FROM posts
LEFT JOIN votes
ON posts.id = votes.post_id
GROUP BY posts.id;
```

**Explanation:**

- `COUNT(votes.post_id)`: Counts the number of votes for each post.
- `GROUP BY posts.id`: Groups the results by post ID.
- If a post has no votes, `vote_count` will be `0`.

## Filtering for a Specific Post

To retrieve the vote count for a specific post, add a `WHERE` clause.

**Query:**

```sql
SELECT posts.*, COUNT(votes.post_id) AS vote_count
FROM posts
LEFT JOIN votes
ON posts.id = votes.post_id
WHERE posts.id = 10
GROUP BY posts.id;
```

**Explanation:**

- `WHERE posts.id = 10`: Filters the results to only include the post with ID `10`.

## Common Pitfalls

1. **Ambiguous Column Names**: Always prefix column names with the table name when joining tables.
2. **Counting Null Values**: Use a specific column (e.g., `votes.post_id`) in `COUNT` to avoid counting `NULL` values.
3. **Join Direction**: Ensure the join direction (`LEFT JOIN`, `RIGHT JOIN`) matches your data requirements.

## Practical Example: Counting Votes per Post

### Query

```sql
SELECT posts.id, posts.title, COUNT(votes.post_id) AS vote_count
FROM posts
LEFT JOIN votes
ON posts.id = votes.post_id
GROUP BY posts.id;
```

### Explanation

- Retrieves the `id` and `title` of each post.
- Counts the number of votes for each post using `COUNT(votes.post_id)`.
- Groups the results by post ID.

## Key Takeaways

1. **Joins** are essential for combining data from multiple tables.
2. Use **left joins** to include all records from the left table, even if there are no matches in the right table.
3. Use **group by** and **count** to aggregate data (e.g., count posts or votes).
4. Always handle **ambiguous column names** by prefixing them with the table name.

## Resources

- [PostgreSQL Tutorial: Joins](https://neon.tech/postgresql/postgresql-tutorial/postgresql-joins)
- Practice with sample tables to understand joins better.

[[TOC]]
