[[TOC]]

# Notes on Python API Development Course

## Course Overview

- **Instructor**: [Sanjeev Thiagarajan](https://www.youtube.com/watch?v=0sOvCWFmrtA)
- **Course Duration**: 19 hours.
- **Objective**: Develop a comprehensive understanding of Python API development, including:
  - Authentication
  - CRUD (Create, Read, Update, Delete) operations
  - Schema validation
  - API documentation

### Why This Course Is More Than Just API Development

- **Extensive Coverage of SQL**:
  - Basics of databases and SQL.
  - Core concepts like primary keys, foreign keys, and table constraints.
  - Generating and integrating database schemas with APIs.
  - Using both raw SQL queries and ORMs (Object-Relational Mappers).
- **Tooling and Testing**:
  - Database migration tools (e.g., Alembic).
  - Tools like Postman for testing HTTP packets.
  - Automated integration tests to ensure code reliability.
- **Deployment**:
  - Deploy on Ubuntu machines via cloud providers (AWS, GCP, Azure, etc.).
  - Deploy using Heroku’s free tier for cost-effective hosting.
  - Dockerization for containerized deployment.
  - CI/CD pipelines using GitHub Actions for automated testing and deployment.

## Tech Stack

### Framework: FastAPI

- **Why FastAPI?**
  - API-first approach.
  - High performance and ease of use.
  - Auto-documentation feature simplifies API maintenance and reduces errors.
  - Popular among modern developers for its interactive and efficient design.

### Database: PostgreSQL

- Chosen for its reliability and compatibility.
- Supported by rich documentation and community resources.

### ORM: SQLAlchemy

- Industry-standard for Python.
- Simplifies database interactions and supports migration to more complex systems.

### Testing and Tools

- Postman for HTTP testing.
- Alembic for database migration.
- CI/CD with GitHub Actions for streamlined development.

## Project Overview

### Application Purpose

- Develop a social media API.
- Users can perform CRUD operations on posts and vote on others' posts.

### Features

#### Core Endpoints

1. **Posts**:
   - Retrieve all posts.
   - Retrieve a specific post.
   - Create, update, and delete posts.
2. **Users**:
   - Create users.
   - Retrieve user information.
3. **Authentication**:
   - Login endpoint for user authorization.
4. **Voting**:
   - Like or upvote specific posts.

#### Built-In Documentation

- FastAPI generates interactive documentation automatically.
- Test API endpoints directly from the documentation interface.

### Key Functionalities

- **Authentication**: Users must log in to access or modify data.
- **CRUD Operations**: Covers all actions required for managing posts.
- **Voting System**: Adds interactivity and simulates social media engagement.

### Practical Demonstrations

- **User Creation**:
  - Example inputs include email and password.
  - API returns a success response (e.g., HTTP 201) with user details.
- **Post Management**:
  - Examples of creating posts with titles, content, and optional parameters like publishing status.
  - Responses include detailed information about the post and its creator.

## Learning Outcome

By the end of the project, learners will be equipped to:

- Build robust APIs with user authentication and data management features.
- Integrate SQL databases into APIs and perform advanced queries.
- Utilize modern tools for deployment and testing.
- Apply the concepts to create scalable and secure APIs for various applications.
