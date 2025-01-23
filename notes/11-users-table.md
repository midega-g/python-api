# Creating User Functionality

- In this section, we focus on implementing user functionality, including user registration, login, and associating posts with specific user accounts.
- The primary objective is to enable users to create accounts and interact with the application.

## User Registration

### Step 1: Define the User Model

1. **Create a Table in the PostgreSQL Database**
   - In the `models.py` file, define a SQLAlchemy ORM model for the `users` table.
   - The model represents how user data is stored in the database.

2. **User Class**

   ```python
    class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True, nullable=False, index=True)
        email = Column(String, nullable=False, unique=True)
        password = Column(String, nullable=False)
        created_at = Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')
        )
   ```

   - `id`: Unique identifier for each user.
   - `email`: Must be unique and not null.
   - `password`: Required but does not need to be unique.
   - `created_at`: Automatically records when the user was created.

3. **Verify the Table Creation**
   - After defining the model, refresh the database to confirm the `users` table is created with all constraints (e.g., unique email constraint).
   - Test the table by inserting a user and ensuring duplicate emails throw an error.

### Step 2: Create a Path Operation for User Registration

1. **Define the Path Operation**

    In `main.py`, define the following:

   ```python
      @app.post("/users", status_code=status.HTTP_201_CREATED)
      def create_user(user: UserCreate = Body(...), db: Session = Depends(get_db)):
          new_user = User(**user.model_dump())
          db.add(new_user)
          db.commit()
          db.refresh(new_user)
          return new_user
   ```

   - URL path: `/users`
   - HTTP method: POST
   - Status code: `201` (Created)

2. **User Schema for Validation**
   - In `schema.py`, define a Pydantic schema for the request data to validate the email and password.

   ```python
   class UserCreate(BaseModel):
       email: EmailStr
       password: str
   ```

   - `EmailStr`: Ensures the email is valid (requires the `email-validator` library).
   - `password`: Basic string validation.

3. **Test the Endpoint**
   - Use Postman or a similar tool to send a POST request:

     ```json
     {
         "email": "example@gmail.com",
         "password": "password123"
     }
     ```

   - Verify the user is created in the database and confirm the email constraint works.

### Step 3: Enhance Security and Responses

1. **Prevent Returning the Password**
   - Define a separate response schema in `schemas.py` to exclude the password from the response.

   ```python
   class UserResponse(BaseModel):
      id: int
      email: EmailStr
      created_at: datetime
   ```

   - Update the path operation to use the `UserOut` schema as the response model.

   ```python
   @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
      def create_user(user: UserCreate = Body(...), db: Session = Depends(get_db)):
          new_user = User(**user.model_dump())
          db.add(new_user)
          db.commit()
          db.refresh(new_user)
          return new_user
   ```

2. **Test the Updated Response**
   - Confirm the response includes only `id`, `email`, and `created_at`.

3. **Add Validation for Email**
   - Test invalid emails (e.g., "invalidemail") and ensure the validator rejects them with an appropriate error message.

## Password Hashing and FastAPI Implementation

### Key Points

1. **Issue with Storing Plain Text Passwords:**
   - Storing plain text passwords in a database is a major security risk.
   - If the database is hacked or leaked, plain text passwords can be exploited.

2. **Solution: Hashing Passwords:**
   - Hash passwords before storing them in the database.
   - A hash is a one-way transformation that cannot be reversed to retrieve the original password.

3. **Libraries Required:**
   - Specify the `bcrypt` algorithm, which is widely used and secure.
   - Installation command:

   ```bash
   pip install bcrypt
   ```

4. **Setting Up Password Hashing:**
   - In the `utils.py` file, import necessary modules and define the hashing context together with a function:

     ```python
     import bcrypt

     def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
     ```

5. **Hashing the Password in User Registration:**
   - Before saving the user data, import the `hash_password` from `utils.py` file and include the following lines in the post router when creating a user
   - Note that `create_new_user` is a function used for creating user that follows the logic that was defined earlier on, only that it handles exceptions where email already exists

     ```python
     from .utils import hash_password, create_new_user

     @app.post("/users",  ...) # code omitted for brevity
      def create_user(user: UserCreate = Body(...), db: Session = Depends(get_db)):
          user.password = hash_password(user.password)
          return create_new_user(db, user.model_dump())
     ```

6. **Testing the Implementation:**
   - Register a new user and verify that the password is stored as a hash in the database.

## Fetching a Single User Information

1. **Purpose of the Route:**
   - Retrieve user information by ID.
   - Useful for authentication or viewing user profiles.

2. **Setting Up the Route:**

   ```python
   @app.get("/users/{id}", response_model=schemas.UserOut)
   def get_user(id: int, db: Session = Depends(get_db)):
       user = db.query(models.User).filter(models.User.id == id).first()
       if not user:
           raise HTTPException(status_code=404, detail=f"User with id {id} does not exist")
       return user
   ```

3. **Testing the Route:**
   - Test the GET endpoint with a valid user ID.
   - Ensure the response excludes the password field.

### Handling the Password Field in the Response

1. **Avoid Returning Passwords:**
   - Returning even hashed passwords in responses is insecure.
   - Use a schema that excludes the password field, e.g., `UserResponse` schema:

     ```python
     class UserResponse(BaseModel):
        id: int
        email: EmailStr
        created_at: datetime
     ```

2. **Set the Response Model:**

   ```python
   @app.get("/users/{user_id}", response_model=UserResponse)
   def get_user(user_id: int, db: Session = Depends(get_db)):
      user = db.query(User).filter(User.id == user_id).first()
      if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with {user_id} not found")
      return user
   ```

3. **Fixing Errors:**
   - Ensure the response model is set in the decorator, not in the function parameters.
   - Confirm that the password field is excluded in the response.

4. **Final Test:**
   - Verify the endpoint only returns allowed fields (e.g., `id`, `email`, etc.) without the password.

[[TOC]]
