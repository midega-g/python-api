# User Login Verification Process

When handling user login, the process involves verifying the user's credentials while maintaining security best practices. The password submitted by the user (in plain text) needs to be verified against the hashed password stored in the database without directly comparing the two.

## Key Takeaways

### Login Endpoint Workflow

- The user provides an email and password in plain text.
- The system retrieves the user's data, including the hashed password, from the database based on the email.
- The provided plain text password cannot be directly compared to the hashed password due to hashing being a one-way process.

### Password Verification

- The plain text password provided by the user is hashed using the same algorithm and compared to the stored hashed password.
- If the hashed version matches, the credentials are considered valid.
- The `bcrypt` algorithm is used for password hashing and verification.

### Security Best Practices

- Avoid revealing whether an invalid login attempt was due to an incorrect email or password.
- Return a generic "Invalid credentials" error message for failed login attempts.

### Separation of Concerns

- Authentication routes are stored in a separate file (e.g., `auth.py`) to differentiate from user-related routes (e.g., `users.py`).
- Utility functions, like password verification, are stored in a dedicated `utils` file for better organization and maintainability.

### Code Snippets

#### 1. Password Verification Function (`utils.py`)

```python
# utils.py
import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
```

#### 2. Login Path Operation (`auth.py`)

```python
# auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserLogin
from app.utils import verify_password

router = APIRouter(tags=["authentication"])

@router.post("/login")
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User).filter(User.email == user_credentials.username).first()
    )

    if not user or not verify_password(
        user_credentials.password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect email or password",
        )
    # Token generation logic goes here
    return {"token": "example token"} # test line
```

#### 3. Schema Definition for User Login (`schemas.py`)

```python
# schemas.py
from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

### Steps to Test

1. **Setup Database**:
   - Ensure the users table contains hashed passwords.
   - Clear any non-hashed password data to avoid issues.

2. **Add Router to Main File**:
   - Import the authentication router in `main.py`:

     ```python
     from .routers import auth

     app.include_router(auth.router)
     ```

3. **Testing Scenarios**:
   - Test with correct email and password: Should return the hard-coded message above.
   - Test with incorrect password: Should return "Invalid credentials."
   - Test with non-existing email: Should return "Invalid credentials."

## Creating the Access Token

To handle signing and verifying JWT tokens, we need to install `PyJWT`

```bash
pip install PyJWT
```

- We'll create a new file named `oauth2.py` to manage authentication and JWT tokens and import the required modules

```python
import jwt
from datetime import datetime, timedelta
```

- We need three key pieces of information for token generation:

  1. **Secret Key** - A special key stored only on the server to verify data integrity which can be generated from the terminal with the command:

      ```python
      openssl rand -hex 32
      ```

  2. **Algorithm** - The hashing algorithm used (we'll use `HS256`).
  3. **Expiration Time** - The duration for which the token remains valid.

      ```python
      SECRET_KEY = "your_secret_key_here"
      ALGORITHM = "HS256"
      ACCESS_TOKEN_EXPIRE_MINUTES = 30
      ```

- We then define a function that generates a JWT (JSON Web Token) for user authentication.

  ```python
  def create_access_token(data: dict, expires_delta: timedelta | None = None):
      to_encode = data.copy()
      if expires_delta:
          expire_time = datetime.now(timezone.utc) + expires_delta
      else:
          expire_time = datetime.now(timezone.utc) + timedelta(
              minutes=ACCESS_TOKEN_EXPIRE_MINUTES
          )
      to_encode.update({"exp": expire_time})
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
      return encoded_jwt
  ```

- It takes in:
  - `data`: A dictionary containing the payload (e.g., user ID, roles).
  - `expires_delta`: An optional timedelta object specifying how long the token should be valid. If `None`, a default expiration time is used.
- It then ensure that the data dictionary is copied to prevent modifying the original data.
- If `expires_delta` is provided, the expiration time is `now + expires_delta`.
- If it is not provided, it defaults to `ACCESS_TOKEN_EXPIRE_MINUTES` (a predefined value).
  - `datetime.now(timezone.utc)` ensures the time is in UTC.
- The expiration time is added to the payload under the `"exp"` key.
  - This makes the token time-limited.
- The `jwt.encode` function:
  - Takes the `to_encode` dictionary as the payload.
  - Uses `SECRET_KEY` to sign the token (ensuring data integrity).
  - Uses `ALGORITHM` (e.g., "HS256") for encryption.

## Using the Access Token in FastAPI

- Import the function into `auth.py` and replace the hard-coded return statement in the `login` function as show below

```python
from app.oauth2 import create_access_token

def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db),
):
    # other code logic goes here

    access_token = create_access_token(data={"user_id": user.id}, expires_delta=60)
    return {"access_token": access_token, "token_type": "bearer"}
```

- Note that we use only the user ID to generate the token, but you can provide other values as long as they are to expose the user to security breaches given that the generated token is visible

!!! Testing the Token

- Once valid email address and password are provided in the login route, copy the generated token.
- Go to Postman's *Authorization* tab and under *Auth Type*, select *Bearer Token*.
- Paste the token the *Token* field

## Implementing `OAuth2PasswordRequestForm`

We are modifying the login route to use the built-in `OAuth2PasswordRequestForm` utility in the FastAPI library for handling user credentials. This makes the process more streamlined and leverages FastAPI's built-in functionality.

### Benefits

1. **Streamlined Process**: Reduces the need for custom logic to parse and validate credentials.
2. **Consistency**: Leverages FastAPI's standardized approach to handling form data.
3. **Flexibility**: Works with any identifier (email, username, ID) by treating it as `username`.

### Key Changes

1. **Importing the Utility**

    - In `auth.py`, import the `OAuth2PasswordRequestForm` from FastAPI's security module:

      ```python
      from fastapi.security import OAuth2PasswordRequestForm
      ```

2. **Updating the Login Route**

    - Instead of accepting user credentials through the request body, we use `OAuth2PasswordRequestForm` as a dependency hence import `Depends` and include it in the `login` function;

      ```python
      from fastapi import Depends

      @router.post("/login")
      def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
          user = db.query(User).filter(User.email == user_credentials.username).first()
          # other code logic goes here

          return {"access_token": access_token, "token_type": "bearer"}
      ```

3. **Adapting Field Access**

    - The `OAuth2PasswordRequestForm` utility automatically extracts credentials from form data.
    - It stores the credentials in two fields:
      - `username`: The identifier (e.g., email, username, ID).
      - `password`: The user's password.

    - Therefore, since it does not have an `email` field but instead uses `username` as a generic identifier, we are going to retrieve the user's email (if used as the identifier), refer to `user_credentials.username`.

      ```python
      user = db.query(User).filter(User.email == user_credentials.username).first()
      ```

### Testing Changes

- **Old Method**: Credentials were sent in the request body.
- **New Method**: Credentials must be sent as form data hence use Postman's `form-data` option under the `Body` tab.

!!! Common Error

- If credentials are sent in the body instead of form data, the following error occurs:

  ```json
  {
    "detail": "username is field required. Value error missing"
  }
  ```

Ensure credentials are included in form data, not the body.

## Logging in a User

- The following sequence is common:
  - Send a request to the login endpoint with a username and password.
  - The API returns an **access token**.
  - The user includes the **JWT token** in requests to access protected endpoints.
  - The API validates the token before granting access.

- The validation is done to check that the token:
  - Is still **valid**.
  - Has not been **tampered** with.
  - Has not **expired**.

### Defining Token Schema

- However, before these events, we need to ensure that we define a schema to structure the expected token data in the `schemas.py` as follows:

  ```python
  class Token(BaseModel):
      access_token: str
      token_type: str
  ```

- This represents the actual token response that the server returns to the client after successful authentication.
- `token_type` is usually "bearer" for OAuth2.
- The syntax look like:

  ```json
  {
      "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
      "token_type": "bearer"
  }
- Now we can update the router to be:

    ```python
    from app.schemas import Token

    @router.post("/login", response_model=Token)
    def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        user = db.query(User).filter(User.email == user_credentials.username).first()
        # other code logic goes here

        return {"access_token": access_token, "token_type": "bearer"}
    ```

- Also we need to define a schema for token data still in the `schemas.py` as follows:

  ```python
  class TokenData(BaseModel):
      user_id: str | None = None
  ```

- This is used internally by the server to extract and validate data from the token.
- Used for user identification in protected routes.
- In this case, `user_id` is optional (`None` if missing).
- This schema is used in the `verify_token()` function created in the next step

### Verifying the Access Token

- With the schema defined, we need to create a function `verify_access_token` in `oauth2.py`:

  ```python
  from jwt import InvalidTokenError
  from app.schemas import TokenData

  def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")  # pylint: disable=redefined-builtin
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError as exc:
        raise credentials_exception from exc
    return token_data
  ```

- This function:
  - Decodes the JWT token using the secret key and algorithm.
  - Extracts the `user_id` from the token's payload.
  - Raises an exception if the token is invalid or missing the `user_id`.
  - Returns a TokenData object containing the extracted `user_id`.
- The function is then used in the `get_current_user()` (defined next) to verify and extract user data from the token.
- It ensures the token is valid, unexpired, and signed before using it.

### Getting the Current User

- We also define a function `get_current_user` in the same file:

  ```python
  from fastapi.security import OAuth2PasswordBearer

  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
      credential_exception = HTTPException(
          status.HTTP_401_UNAUTHORIZED,
          detail="Could not validate credentials",
          headers={"WWW-Authenticate": "Bearer"},
      )
      token = verify_token(token, credential_exception)
      user = db.query(User).filter(User.id == token.user_id).first()
      return user
  ```

- The function:
  - Uses `OAuth2PasswordBearer` to extract the token from the request.
  - Calls `verify_token()` to validate and decode the token.
  - Queries the database to retrieve the user based on the `user_id` from the token.
  - Returns the authenticated user object (or raises an exception if not found).

### Protecting Endpoints

- The `get_current_user()` function is then used in protected API routes to retrieve the currently logged-in user.
- For instance to ensure that only authenticated users can create a post from the the post endpoint in our API, the code is adjusted as follows:

  ```python
  @router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
  def create_post(current_user: str = Depends(get_current_user), ...) # for brevity purposes
      # other code logic goes here
      return new_post
  ```

  - The `Depends(get_current_user)` function ensures that only authenticated users can access the endpoint.
  - It calls the `get_current_user()` function which calls the `verify_access_token()` function
    - If the token is valid, the user is granted access.
    - If invalid, a **401 Unauthorized** error is returned.

[[TOC]]
