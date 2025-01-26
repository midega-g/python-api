[[TOC]]

# FastAPI Basics, Postman, and HTTP Request Functions

# Introduction to FastAPI

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Setting Up FastAPI

1. **Install FastAPI:**
   - Basic installation:

     ```bash
     pip install fastapi
     ```

   - Install with all optional dependencies:

     ```bash
     pip install fastapi[all]
     ```

     The `all` flag ensures dependencies like `uvicorn` (ASGI server) and others (e.g., `bcrypt`, `graphql`) are installed.

2. **Verify Installation:**
   - Use `pip freeze` to see all installed packages.
   - Example dependencies include:
     - `uvicorn`: Web server.
     - `bcrypt`: For cryptography.
     - `graphql`: If using GraphQL endpoints.

3. **Understanding File Structure:**
   - Installed libraries and dependencies reside in the `lib` folder of your virtual environment.

## Writing First FastAPI Application

1. **Import and Create an Instance:**

   ```python
   from fastapi import FastAPI

   app = FastAPI()
   ```

   - `FastAPI()` creates an instance of the application. While you can name it anything, `app` is the convention.

2. **Define a Path Operation:**

   ```python
   @app.get("/")
   def root():
       return {"message": "Hello, World!"}
   ```

   - **`@app.get("/")`**: A decorator defining an endpoint for the root path (`/`) using the HTTP `GET` method.
   - **`root()`**: The function executed when the endpoint is accessed.
   - **Return Statement**: The returned dictionary is converted to JSON.

3. **Running the Application:**

   **a. Running Uvicorn Without Packaging:**
   - Use `uvicorn` to run your FastAPI app:

     ```bash
     uvicorn main:app --reload
     ```

     - **`main`**: Refers to the name of the Python file (`main.py` without the `.py` extension) containing the FastAPI instance.
     - **`app`**: Refers to the FastAPI instance created in the script.
     - **`--reload`**: Enables live reloading, automatically restarting the server whenever the code changes. Useful during development.

   - Access the app at `http://127.0.0.1:8000/`.

   **b. Running Uvicorn with a Package Structure:**
   - Restructure the project by creating a folder for the application code. For example, create a folder named `app` and move the `main.py` file into it.
   - Convert the folder into a Python package by adding an empty file named `__init__.py` inside the folder:

     ```bash
     mkdir app
     mv main.py app/
     touch app/__init__.py
     ```

   - Update the `uvicorn` command to include the package name:

     ```bash
     uvicorn app.main:app --reload
     ```

     - **`app`**: Refers to the package folder.
     - **`main`**: Refers to the `main.py` file inside the `app` folder.
     - **`app`**: Refers to the FastAPI instance created in the script.

4. **Verify Output:**
   - Verify that the application runs correctly by accessing it at `http://127.0.0.1:8000/`
   - In this case you should see `{"message": "Hello, World!"}`.

## Using Postman to Test APIs

- Postman is a popular tool to test APIs without a browser.
- It enables sending HTTP requests and viewing responses.

### Steps to Use Postman

1. **Install Postman:**
   - Download from [Postman’s official site](https://www.postman.com/downloads/).

2. **Create a New Request:**
   - Open Postman and click **New** > **Request**.
   - Select HTTP method (GET, POST, etc.).
   - Enter the URL (e.g., `http://127.0.0.1:8000/`).

3. **Send the Request:**
   - Click **Send** to receive the response.
   - View response body, headers, and status code in Postman’s interface.

4. **Advanced Features:**
   - **Authorization:** Add tokens or credentials.
   - **Body:** Add JSON or other payloads for POST/PUT requests.
   - **Collections:** Group related API requests and saving them with memorable names

# Understanding FastAPI Code Syntax

## Path Operations

Terminology used in FastAPI to describe routes (endpoints)

- It has the following syntax:

   ```python
   @app.get("/items")
   async def get_items():
      return ["item1", "item2"]
   ```

- From the syntax, FastAPI consist of:
  - **Decorator:** Specifies the HTTP method and route.
  - **Function:** Contains the logic and return value for the endpoint.

1. **Decorators:**
   - They transform functions into API endpoints.

     ```python
     @app.get("/")
     ```

   - Supported HTTP methods include:
     - `@app.get`
     - `@app.post`
     - `@app.put`
     - `@app.delete`

2. **Functions:**
   - Regular Python functions, optionally asynchronous (`async`).
   - Example:

     ```python
     def root():
         return {"message": "Hello, World!"}
     ```

3. **Asynchronous Functions (Optional):**
   - Use `async def` for tasks like database queries or external API calls.

## Naming Conventions in FastAPI

1. **File Names:**
   - Use descriptive names like `main.py` or `app.py`.

2. **Function Names:**
   - Reflect the purpose of the endpoint.
   - Example:

     ```python
     def get_user_profile():
     ```

3. **Decorators:**
   - Match HTTP methods and paths logically.
   - Example:

     ```python
     @app.post("/create-user")
     ```

# HTTP Request Functions and Their Application in FastAPI

[HTTP methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) define the type of operation performed on a resource:

1. **GET:** Retrieve data.

   ```python
   @app.get("/items")
   def get_items():
       return {"items": ["item1", "item2"]}
   ```

2. **POST:** Create new resources.

   ```python
   @app.post("/items")
   def create_item(item: dict = Body(...)):
       return {"received_item": item}
   ```

3. **PUT:** Update existing resources.

   ```python
   @app.put("/items/{item_id}")
   def update_item(item_id: int, item: dict = Body(...)):
       return {"item_id": item_id, "updated_item": item}
   ```

4. **DELETE:** Remove resources.

   ```python
   @app.delete("/items/{item_id}")
   def delete_item(item_id: int):
       return {"message": f"Item {item_id} deleted"}
   ```

## More about `POST` Request

- `POST` requests differ from `GET` requests primarily in their functionality and purpose.
- A `GET` request retrieves data from the API server, whereas a `POST` request sends data to the API server for processing or creating new resources.
- For example, a `POST` request can be used to create a new social media post by sending the title, content, and user details to the API server.

- **Steps to Create a POST Request Using Postman:**
  1. Open Postman and create a new request.
  2. Select the HTTP method as "POST".
  3. Enter the URL for the API endpoint (e.g., `<url>/createposts`).
  4. Navigate to the "Body" tab in Postman.
  5. Select "raw" and then choose "JSON" from the dropdown.
  6. Provide the payload in JSON format (e.g., `{ "title": "Top Beaches in Florida", "content": "Check out these awesome beaches" }`).
  7. Hit the "Send" button to execute the request.

- **What Happens When the "Send" Button is Hit?**
  - The JSON payload is sent to the API server.
  - The server processes the payload, interacts with a database (if applicable), and sends back a response.
  - In this example, the server responds with a confirmation message or the created post details.

- **Explaining the Code:**

```python
from fastapi import FastAPI, Body

app = FastAPI()

@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}
```

- The `Body` import from FastAPI is used to explicitly define and validate the request body.
- `payload: dict = Body(...)` specifies that the incoming request body must be a dictionary and is required.
- The function `create_post` processes the payload, extracts its data, and returns a response containing the new post's details.

- **Use Case for POST Method:**
  - The POST method is ideal for creating resources on the server, such as new posts, user accounts, or transactions.
  - It allows sending complex data to the API server, enabling operations like adding new entries to a database.

- **Key Differences Between GET and POST Requests:**
  - GET requests fetch data, while POST requests send data to be processed.
  - GET requests have no body, whereas POST requests include a body containing the data to be sent.
  - GET is used for retrieval, and POST is used for creation or updates.

- **Sending Data in the Body:**
  - Within Postman, data can be sent in the "Body" section as JSON.
  - JSON format closely resembles Python dictionaries, with key-value pairs enclosed in curly braces.

- **Output When Sending a POST Request:**
  - If the payload contains `{ "title": "Top Beaches in Florida", "content": "Check out these awesome beaches" }`, the API server responds with:

    ```json
    {
        "new_post": "title: Top Beaches in Florida, content: Check out these awesome beaches"
    }
    ```

- **Next Steps in a Real Application:**
  - The server would typically store the data in a database.
  - Future GET requests could retrieve the newly created post from the database.

- **Best Practices:**
  - Avoid using unconventional endpoints like `/createposts`; prefer RESTful conventions (e.g., `POST /posts`).
  - Always validate and sanitize incoming data to prevent errors and security vulnerabilities.

- **Advantages of Using `Body` in FastAPI:**
  - Enhances clarity by explicitly defining request bodies.
  - Provides built-in validation and parsing of payloads.
  - Improves API documentation with clear parameter definitions.
