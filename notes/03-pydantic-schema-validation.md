# Pydantic and FastAPI

## Introduction

This lecture covers the importance of Pydantic in FastAPI for data validation and schema definition, ensuring that front-end data adheres to specific rules and formats. This prevents arbitrary or invalid data from being processed by the backend.

## Issues in Current Workflow

1. Extracting multiple values from the body is cumbersome.
2. Arbitrary data can be sent by the client.
3. Data is not validated (e.g., blank titles are allowed).
4. There is no defined schema as a contract between the front end and back end.

## Solution: Pydantic for Schema Validation

FastAPI leverages Pydantic to define schemas, validate input data, and ensure API requests adhere to a structured contract.

### Key Steps and Code Examples

#### Install and Import Pydantic

Pydantic is installed by default when installing FastAPI. Check by locating it in the `lib` folder.

```python
from pydantic import BaseModel, PositiveInt
```

#### Define a Pydantic Model

Define a schema for incoming data by creating a class that extends `BaseModel`.

```python
class Post(BaseModel):
    title: str  # Title of the post (string type)
    content: str  # Content of the post (string type)
```

This schema ensures that incoming data must include a `title` and `content`, both as strings.

#### Use Pydantic Model in Path Operation

Replace the manual payload extraction with the Pydantic model:

```python
@app.post("/posts")
def create_post(post: Post = Body(...)):
    print(post.title)         # Access and prints title to console
    print(post.content)       # """ content to console
    print(post.model_dump())  # """ the whole post as a dict to console
    return post
```

- **Validation:** FastAPI validates incoming requests based on the `Post` schema.
- **Automatic Error Messages:** If data doesn't meet the schema, FastAPI returns a `422 Unprocessable Entity` error with details.

#### Example Outputs in Postman

- **Missing Title:**
  - Error: `"title": "field required"`
- **Invalid Data Type:**
  - Error: `"title": "value is not a valid string"`
- **Valid Input:**
  - Response: `{"title": "Top beaches in Florida", "content": "Details about beaches"}`
  - Note that without the `.model_dump()` the response is not a JSON or a dictionary

### Optional Fields with Defaults

Add optional fields with default values:

```python
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # Defaults to True
```

- **Behavior:** If `published` is not provided, it defaults to `True`.
- Also if the value `1` is provided, it is converted to `True` while `0` is converted to `False`; any other value give an error

#### Fully Optional Fields

Define fields that default to `None` if not provided:

```python
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[PositiveInt] = None  # Fully optional
```

- **Behavior:** `rating` can be omitted or set to `None`.
- **Validation:** If `rating` is provided, it must be a positive integer.

If only the title and content are specified (using Postman), then this would give something like this:

```python
{'title': 'top beaches in florida', 'content': 'check this awesome beaches', 'published': True, 'rating': None}
```

### Convert to Dictionary

Convert the Pydantic model to a dictionary for easy manipulation:

```python
@app.post("/posts")
def create_post(post: Post = Body(...)):
    return post.model_dump()  # Converts model to dictionary
```

This allows returning data in a common format for APIs.

## Conclusion

By using Pydantic with FastAPI:

- Input data is validated automatically.
- Errors are returned clearly and concisely.
- Schemas provide a contract between the backend and frontend.

Future lessons will extend the use of Pydantic for output validation and more complex scenarios.
