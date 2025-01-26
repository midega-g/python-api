# SQL Queries Basics

## Step-by-Step Guide for SQL Basics

### 1. **Setting Up the Database for Queries**

- Create additional entries in your database before running queries to ensure data variability:
  - Vary prices.
  - Mix `true` and `false` values for Boolean fields.
  - Use different inventory numbers.
  - Add entries with different timestamps.
  - Adding, for instance, TV items (e.g., TV Blue, TV Red, TV Yellow) with specific prices.
- This ensures diverse query results.

### 2. **Accessing the Query Tool**

- Right-click on your database (e.g., `fast_api`).
- Select `Query Tool` to open a new tab for running queries.

### 3. **Running the First Query**

- Use the query:

     ```sql
     SELECT * FROM products;
     ```

- Click the play button to execute the query.
- This retrieves all rows and columns from the `products` table.

### SQL Syntax Breakdown

**Query:**

```sql
SELECT * FROM products;
```

- **`SELECT`**: Specifies which columns to retrieve
- **`*`**: Wildcard symbol that selects all columns
  - For databases with many columns, avoid using `*` to improve query efficiency and readability.
- **`FROM`**: Indicates the table to query (e.g., `products`).
- **`;`**: Terminates the SQL statement.
  - Ensure all SQL statements end with a semicolon (`;`).
  - Using `pgAdmin`, a missing semicolon may still work, but it is mandatory in the command line.

**Example Query Results:**

- When executed, the query retrieves all data from the `products` table, displaying all rows and columns.

## Filtering Columns

- To retrieve specific columns:

  ```sql
  SELECT name, price FROM products;
  ```

- Example Output:
  - Columns displayed: `name`, `price`.

- Ordering columns:

  ```sql
  SELECT id, name, price FROM products;
  ```

  - Columns appear in the specified order: `id`, `name`, `price`.

## Capitalization Rules

- SQL keywords (`SELECT`, `FROM`) can be capitalized or lowercase.
- Best practice: Use capitalization for SQL keywords to differentiate them from user-defined table/column names.
- Example:

  ```sql
  SELECT name FROM products;
  ```

  - `SELECT` and `FROM` are SQL keywords.
  - `name` and `products` are user-defined names.

## Renaming Columns

- Use the `AS` keyword to rename columns in the query output:

  ```sql
  SELECT id AS product_id, is_sale AS on_sale FROM products;
  ```

- Example Output:
  - Renamed columns: `id` -> `product_id`, `is_sale` -> `on_sale`.

!!! Practical Examples

1. **Retrieve All Data**

    ```sql
    SELECT * FROM products;
    ```

    - Retrieves all rows and columns from the `products` table.

2. **Retrieve Specific Columns**

    ```sql
    SELECT name, price FROM products;
    ```

    - Displays only `name` and `price` columns.

3. **Rename Columns**

    ```sql
    SELECT id AS product_id, name, price FROM products;
    ```

    - Renames `id` to `product_id` in the output.

## SQL Notes: Filtering and Querying Data

### Step-by-Step Guide to Filtering Data in SQL

#### 1. **Retrieve All Columns**

```sql
SELECT * FROM products;
```

- `*`: Selects all columns from the table.

#### 2. **Select Specific Columns**

```sql
SELECT ID, name FROM products WHERE ID = 3;
```

- Lists only the `ID` and `name` columns for rows matching the condition.

#### 3. **Filtering Rows Using Specific Criteria**

- **Filter by Primary Key:**

```sql
SELECT * FROM products WHERE ID = 10;
```

- `WHERE`: Specifies the filter condition.
- `ID = 10`: Matches rows where the `ID` column equals 10.

- **Find Products with Zero Inventory:**

```sql
SELECT * FROM products WHERE inventory = 0;
```

- **Filter by Name (String Matching):**

```sql
SELECT * FROM products WHERE name = 'TV';
```

- Use single quotes for string values.
- Missing quotes results in an error.

#### 4. **Using Comparison Operators**

- **Greater Than or Less Than:**

```sql
SELECT * FROM products WHERE price > 50;
```

- Retrieves rows where `price` is greater than 50.

- **Greater Than or Equal To:**

```sql
SELECT * FROM products WHERE price >= 80;
```

- **Less Than or Equal To:**

```sql
SELECT * FROM products WHERE price <= 80;
```

- **Not Equal To:**

```sql
SELECT * FROM products WHERE inventory != 0;
```

- Alternative syntax: `inventory <> 0`.

#### 5. **Combining Conditions with AND/OR**

- **AND Operator:**

```sql
SELECT * FROM products WHERE inventory > 0 AND price > 20;
```

- Matches rows where both conditions are true.

- **OR Operator:**

```sql
SELECT * FROM products WHERE price > 100 OR price < 20;
```

- Matches rows where at least one condition is true.

#### 6. **Filter by Multiple Values Using IN**

- **Retrieve Rows with Specific IDs:**

```sql
SELECT * FROM products WHERE ID IN (1, 2, 3);
```

- More concise than using multiple OR conditions.

#### 7. **Filtering with LIKE for Pattern Matching**

- **Retrieve all items starting with "TV":**

```sql
SELECT * FROM products WHERE name LIKE 'TV%';
```

- The `%` sign matches any sequence of characters after "TV".

- **Retrieve all items ending with "E":**

```sql
SELECT * FROM products WHERE name LIKE '%E';
```

- **Retrieve all items containing "EN":**

```sql
SELECT * FROM products WHERE name LIKE '%EN%';
```

- **Negate filtering using `NOT LIKE`:**

```sql
SELECT * FROM products WHERE name NOT LIKE '%E';
```

### Sorting and Limiting Results

#### 1. **Ordering Results with ORDER BY**

- **Sort by price in descending order:**

```sql
SELECT * FROM products ORDER BY price DESC;
```

- **Order by inventory (descending) and price (ascending):**

```sql
SELECT * FROM products ORDER BY inventory DESC, price ASC;
```

- **Sorting by creation timestamp to get the most recent products:**

```sql
SELECT * FROM products ORDER BY created_at DESC;
```

#### 2. **Limiting Rows with LIMIT**

- **Retrieve the first 10 rows:**

```sql
SELECT * FROM products LIMIT 10;
```

- **Retrieve only 2 results for products priced greater than 10:**

```sql
SELECT * FROM products WHERE price > 10 LIMIT 2;
```

#### 3. **Skipping Rows with OFFSET for Pagination**

- **Skip the first 2 rows and return the next 5:**

```sql
SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 2;
```

- Useful in APIs for implementing pagination.

### Combining Filters and Sorting

- **Retrieve products priced above 20, ordered by creation date:**

```sql
SELECT * FROM products WHERE price > 20 ORDER BY created_at DESC;
```

### Practical Considerations

- **Handling Large Datasets:**
  - Avoid retrieving all rows in production environments to prevent performance issues.
  - Use `LIMIT` and `OFFSET` for efficient handling of large tables.

```sql
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 10;
```

By utilizing these SQL keywords and techniques, we can efficiently manage and retrieve data even from large databases while ensuring optimal performance and usability.

## Adding New Entries to a Database Table

### Using SQL to Insert Data

Instead of relying on the GUI in PG Admin, SQL commands are used to add new entries to a database. Here's how it works:

**Basic Syntax:**

```sql
INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...);
```

- `INSERT INTO`: Command to insert a new row.
- `table_name`: Specify the table to insert data into.
- `(column1, column2, ...)`: Specify the columns to insert data for.
- `VALUES (value1, value2, ...)`: Specify the values for each column in the same order.

**Example**
Insert a new product into the `products` table:

```sql
INSERT INTO products (name, price, inventory) VALUES ('Tortilla', 4, 1000);
```

- Inserts a product named "Tortilla" with a price of $4 and inventory of 1000.
- Columns `is_sale` and others not specified use their default values.

### Order Matching

The order of columns in the `INSERT INTO` statement must match the order of values provided. If the order changes, the corresponding values must also be adjusted.

**Example with Reordered Columns:**

```sql
INSERT INTO products (price, name, inventory) VALUES (4, 'Tortilla', 1000);
```

Here, the price is listed first, so it must be the first value provided.

### Returning Inserted Data

To automatically return the newly inserted row(s):

```sql
INSERT INTO products (name, price, inventory)
VALUES ('Car', 10000, 1)
RETURNING *;
```

- `RETURNING *`: Returns all columns of the inserted row.
- You can specify specific columns to return (e.g., `RETURNING id, name`).

### Inserting Multiple Rows

You can insert multiple rows in a single query:

```sql
INSERT INTO products (name, price, inventory)
VALUES
  ('Laptop', 50, 25),
  ('Monitor', 60, 4);
```

This adds two products: a laptop and a monitor.

## Updating Existing Entries

**Basic Syntax:**

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

- `UPDATE`: Command to modify rows.
- `SET`: Specifies the columns to update and their new values.
- `WHERE condition`: Specifies which rows to update.

**Example**
Update a product:

```sql
UPDATE products
SET name = 'Flour Tortilla', price = 40
WHERE id = 25;
```

- Changes the name and price of the product with `id = 25`.

### Returning Updated Data

To return the updated row:

```sql
UPDATE products
SET is_sale = TRUE
WHERE id = 30
RETURNING *;
```

- Returns the updated row after setting `is_sale` to `TRUE`.

### Updating Multiple Rows

To update rows based on a condition:

```sql
UPDATE products
SET is_sale = TRUE
WHERE id > 15;
```

- Sets `is_sale` to `TRUE` for all products with `id > 15`.

Additional scenarios for updating multiple rows:

1. **Update prices for all products above a certain threshold:**

   ```sql
   UPDATE products SET price = price * 1.1 WHERE price > 100;
   ```

2. **Set discontinued products as inactive:**

   ```sql
   UPDATE products SET status = 'inactive' WHERE status = 'discontinued';
   ```

3. **Increase inventory for low-stock products:**

   ```sql
   UPDATE products SET inventory = inventory + 10 WHERE inventory < 5;
   ```

4. **Update multiple fields in a single query:**

   ```sql
   UPDATE products SET price = price * 0.9, is_sale = TRUE WHERE category = 'electronics';
   ```

5. **Update outdated records based on a date condition:**

   ```sql
   UPDATE products SET status = 'archived' WHERE created_at < '2023-01-01';
   ```

## Deleting Entries from a Database Table

### Basic Syntax

```sql
DELETE FROM table_name WHERE condition;
```

- `DELETE FROM`: Command to delete rows.
- `WHERE condition`: Specifies which rows to delete.

**Example**
Delete a product by its ID:

```sql
DELETE FROM products WHERE id = 10;
```

- Deletes the product with `id = 10`.

### Returning Deleted Data

To see the data before deletion:

```sql
DELETE FROM products WHERE id = 11 RETURNING *;
```

- Returns the deleted row's data.

### Deleting Multiple Rows

To delete rows matching a condition:

```sql
DELETE FROM products WHERE inventory = 0;
```

- Deletes all products with an inventory of 0

Additional scenarios for deleting multiple rows:

1. **Delete products priced below a certain threshold:**

   ```sql
   DELETE FROM products WHERE price < 10;
   ```

2. **Delete discontinued products:**

   ```sql
   DELETE FROM products WHERE status = 'discontinued';
   ```

3. **Delete multiple rows using a list of IDs:**

   ```sql
   DELETE FROM products WHERE ID IN (5, 10, 15);
   ```

4. **Delete old records beyond a certain date:**

   ```sql
   DELETE FROM products WHERE created_at < '2023-01-01';
   ```

5. **Delete all products with low inventory and high price:**

   ```sql
   DELETE FROM products WHERE inventory < 5 AND price > 100;
   ```

## Key Takeaways

1. Use `INSERT INTO` to add rows, and ensure the column and value orders match.
2. Use `UPDATE` to modify existing rows, with the option to return the updated data.
3. Use `DELETE FROM` to remove rows, optionally returning the deleted data.
4. The `RETURNING` keyword simplifies getting results from `INSERT`, `DELETE`, or `UPDATE` commands.

[[TOC]]
