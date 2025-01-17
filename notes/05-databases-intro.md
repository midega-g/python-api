# Introduction to Databases

- **Definition:** A database is a collection of organized data that can be easily accessed and managed.
- **Purpose:** Used to store application-related data such as users, posts, etc., on disk for later retrieval.

## Database Management Systems (DBMS)

- Databases are accessed through a DBMS, which:
  - Receives requests to perform operations.
  - Executes the operations on the database.
  - Returns the results to the user.
- **Key Point:** Users do not interact with the database directly; the DBMS acts as an intermediary.

### Types of Databases

1. **Relational Databases (SQL-based):**
   - Examples: PostgreSQL, MySQL, Oracle, SQL Server.
2. **NoSQL Databases:**
   - Examples: MongoDB, Cassandra, Redis.

### Focus on Relational Databases

- The course focuses on PostgreSQL.
- Core concepts learned for PostgreSQL are transferable to other relational databases, as they all use SQL with minor variations.

### Structured Query Language (SQL)

- **Definition:** SQL is the language used to communicate with the DBMS.
- **Process:**
  - Users send SQL statements to the DBMS.
  - The DBMS processes the statements, performs the operations, and returns the results.

### Installing PostgreSQL

- PostgreSQL download link: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Key Notes on Installation:**
  1. PostgreSQL allows the creation of multiple separate databases within a single instance.
  2. Each database is isolated, enabling:
     - One database per application.
     - Multiple databases for a single application in specific scenarios (e.g., multi-tenancy).
  3. The installation process creates a default database named `Postgres` within the instance:
     - Used as a default connection point to the PostgreSQL instance.
     - Can be retained even after creating custom databases.

## Understanding Tables in Relational Databases

### Concept of Tables

- **Definition**: A table represents a subject or event in an application.
- **Example**: In an e-commerce application, tables might include:
  - Users (registered users)
  - Products (items for sale)
  - Purchases (orders made by users)
  - Reviews (feedback on products)

### Relationships Between Tables

- **Relational Nature**: Tables in a relational database are interconnected.
- **Examples**:
  - **Purchases**: Linked to both users and products (e.g., a user’s purchase order contains products).
  - **Social Media**: Posts table linked to the Users table (e.g., a post is created by a user).

### Structure of Tables

1. **Columns**:
   - Represent attributes of the subject.
   - Examples for a Users table:
     - Name
     - Age
     - Gender
     - Email
     - Address (billing or shipping)

2. **Rows**:
   - Represent individual entries in the table.
   - Example:
     - Row 1: User Vanessa
     - Row 2: User Carl

### Data Types in Databases

- Databases use data types similar to programming languages like Python.
- Common data types in Postgres:

| Data Type       | Description                                  | Example Attribute       |
|-----------------|----------------------------------------------|--------------------------|
| Integer         | Whole numbers                               | Total likes on a post    |
| Float           | Decimal numbers                             | (Less commonly used)     |
| Varchar/Text    | Text data (strings)                         | Name, email, address     |
| Boolean         | True/False values                           | Account activation status|
| Array           | List of values (not commonly used)          | Tags for a product       |

### Primary Key

- **Definition**: A column (or group of columns) uniquely identifying each row.
- **Key Points**:
  - Must be unique for each entry.
  - Only one primary key per table (though it can span multiple columns).
  - Common choice: ID column (unique identifier for each entry).
  - Alternatives: Email, phone number, social security number (if unique).

### Constraints

1. **Unique Constraint**:
   - Ensures values in a column are unique.
   - Example: Prevent two users from sharing the same name.

2. **Not Null Constraint**:
   - Prevents a column from being left blank.
   - Example: Ensure every user has an age.

## PGAdmin and PostgreSQL Database Management

- PGAdmin is the GUI tool used to manage PostgreSQL databases.
- It helps in defining tables, creating, modifying, and deleting entries in the database.

### Setting Up PGAdmin

1. **Launch PGAdmin**:
   - Search for PGAdmin in your applications.
   - On the first launch, you will be asked to set a **master password**.
     - This password is for PGAdmin, not the PostgreSQL instance.
     - It allows PGAdmin to store connection passwords for various PostgreSQL instances.
   - The password set here has no relation to the password for PostgreSQL itself.

2. **Connection to PostgreSQL Instance**:
   - PGAdmin automatically connects to a default server called `PostgresQL 13` on installation.
   - You need to provide the **PostgreSQL user password** (the one created during PostgreSQL installation).
   - Optionally, save the password to avoid entering it every time.

3. **Defining a New Server**:
   - Click on `Create Server` to define a new PostgreSQL instance.
   - **Server Name**: Give it a descriptive name (e.g., "My Local Postgres Instance").
   - **Connection Details**:
     - For a local instance, set the host to `localhost`.
     - Provide the **PostgreSQL password** for connection.
     - The default port is `5432` (unless specified otherwise).
     - The default database is `Postgres`.

4. **Add a New Server Manually**:
   - Enter connection details manually (e.g., host, user, password).
   - Set the database name (default is `Postgres`).
   - Use the default **PostgreSQL username** (`postgres`).

5. **Navigating the PGAdmin Interface**:
   - PGAdmin has a variety of menus and features, but you will primarily focus on the **databases** and **tables** sections.

### Creating a New Database

1. **Create a Database**:
   - Right-click on `Databases`, select `Create > Database`.
   - Enter the **Database Name** (e.g., "MyFastAPIDatabase").
   - The underlying SQL query for creating the database is automatically generated.

2. **Use SQL**:
   - PGAdmin generates the SQL command to create the database.
   - Example: `CREATE DATABASE "MyFastAPIDatabase";`

3. **Access Database**:
   - Once created, click on the new database to access it.

### Creating Tables in PGAdmin

1. **Navigate to the `Schemas > Public > Tables` section**:
   - Right-click and select `Create > Table`.

2. **Define Table Structure**:
   - **Table Name**: Enter a name for the table (e.g., "Products").
   - **Columns**: Define columns based on the attributes required for the table.
     - Example columns for `Products`:
       - **Name**: Product name (data type: `character varying`).
       - **Price**: Product price (data type: `numeric`).
       - **ID**: Unique identifier (data type: `serial` for auto-increment).

3. **Column Properties**:
   - **Not Null**: Set to "Yes" to ensure that a value is required for the column.
   - **Primary Key**: Set a unique column (e.g., `ID`) as the primary key for the table.
   - **Serial Type**: Use `serial` for auto-incrementing ID values.

4. **Example Table Structure**:
   - `Products` table could have the following columns:
     - `name` (type: `character varying`).
     - `price` (type: `numeric`).
     - `id` (type: `serial`, primary key).

5. **Save the Table**:
   - After defining the table, click `Save`.
   - The newly created table will appear under `Tables`.

## Working with PostgreSQL: Managing the Products Table

### 1. Viewing and Editing Data

- **Right-click the product table** and select **View/Edit Data**.
- You can:
  - Select **All rows** to fetch every entry (not recommended for large databases).
  - Select **First 100 rows** or **Last 100 rows** to limit the query results.

- If there's no data in the database, it will display an empty table.
- Underlying SQL query is shown in the Query Editor (`SELECT * FROM my_products ORDER BY ID ASC`).

### 2. Creating and Saving Data

- To add data:
  - Select the column, input data (e.g., **TV** with **price $200**).
  - The **ID** column is auto-generated.
  - **Save Data Changes** button stores the data into the database.

- Creating multiple entries:
  - Add additional products like **DVD player** ($80) and **remote** ($10).
  - Bold text indicates unsaved proposed changes.
  - After saving, new rows are added to the table with incremented IDs.

### 3. Handling Errors

- **Empty Price**: If a required column is left blank, such as the **price**, PostgreSQL will throw an error (**null value in column price**).
  - Ensure that a value is entered for required fields.

- **Empty Name**: Similarly, leaving the **name** blank triggers an error (**null value in column name**).

### 4. Adding New Columns

- To add a new column (e.g., **is_sale** for sale status):
  - **Right-click the product table** → **Properties** → **Columns** → **Add Column**.
  - Data type: **Boolean** (True/False).
  - Set **default value** to `false` (not on sale by default).

- **Refreshing the Table**: After adding a column, use **View/Edit Data** to refresh and see the new column.

### 5. Default Values for New Columns

- When adding a new column with a **default value** (e.g., **is_sale** = false), existing rows automatically get the default value.
- **Example**: A newly added **is_sale** column will be populated with `false` for existing entries.

### 6. Adding Inventory Column

- **Inventory** column is added with data type **Integer**.
- If **not null** is set without a default value, an error occurs when existing rows lack values for this column.

- To avoid errors, provide a **default value** for the column (e.g., `0` items in stock).

### 7. Timestamp Column (Created At)

- **Adding Timestamp**: Add a column named **created_at**.
  - **Data Type**: `timestamp with timezone`.
  - **Default Value**: Use `now()` to automatically set the current timestamp when a new entry is added.

- Existing records are populated with the current timestamp as the default value.

- After adding the timestamp column, all future entries will have the timestamp filled automatically when created.

### 8. Final Thoughts on Column Modifications

- Always set **default values** for frequently empty columns (like `is_sale`).
- For critical fields like **inventory**, ensure they don't accept `null` values.
- **Timestamps** are essential for tracking when entries are created and should be included for better data management.
[[TOC]]
