# Cross-Origin Resource Sharing (CORS) in FastAPI

## Overview

- **CORS (Cross-Origin Resource Sharing)**: A security feature implemented by web browsers to restrict how web pages can make requests to a different domain than the one that served the web page.
- **Default Behavior**: By default, web browsers block requests from a web page to an API hosted on a different domain for security reasons.
- **Testing Tools**:
  - **Postman**: Sends requests from your computer, bypassing CORS restrictions.
  - **Web Browser**: Sends requests from the browser, which enforces CORS policies.

## Key Concepts

### 1. **Same-Origin Policy**

- **Definition**: A web browser allows requests only if the web page and the API are hosted on the same domain.
- **Example**:
  - If the API is hosted on `localhost:8000`, a web page hosted on `localhost:8000` can make requests to the API.
  - A web page hosted on `google.com` cannot make requests to `localhost:8000` unless CORS is configured.

### 2. **CORS Error**

- **Scenario**: When a web page tries to make a request to an API on a different domain, the browser blocks the request and throws a CORS error.
- **Example Error**:

  ```plaintext
  Access to fetch at 'http://localhost:8000/' from origin 'https://google.com' has been blocked by CORS policy.
  ```

## Testing CORS in a Web Browser

### Steps to Reproduce CORS Error

1. Open a web browser and navigate to `google.com`.
2. Open the browser's developer tools (right-click → Inspect → Console).
3. Use the `fetch` API to send a request to your API:

   ```javascript
   fetch('http://localhost:8000/')
     .then(res => res.json())
     .then(console.log);
   ```

4. Observe the CORS error in the console.

### Why Does This Happen?

- The request is blocked because the web page (`google.com`) and the API (`localhost:8000`) are on different domains.
- Browsers enforce CORS to prevent unauthorized cross-origin requests.

## Configuring CORS in FastAPI

- **FastAPI** provides built-in support for CORS via the `CORSMiddleware`.

### Steps to Enable CORS

1. **Import CORS Middleware in `main.py`**:

   ```python
   from fastapi.middleware.cors import CORSMiddleware
   ```

2. **Add CORS Middleware to Your App**:

   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://www.google.com"],  # List of allowed origins
       allow_credentials=True,
       allow_methods=["*"],  # Allow all HTTP methods
       allow_headers=["*"],  # Allow all headers
   )
   ```

### Explanation of CORS Parameters

- **`allow_origins`**: A list of domains allowed to access your API.
  - Example: `["https://www.google.com", "https://www.youtube.com"]`.
  - Use `["*"]` to allow all domains (not recommended for production).
- **`allow_methods`**: A list of HTTP methods allowed (e.g., `GET`, `POST`, `PUT`, `DELETE`).
  - Example: `["GET", "POST"]`.
- **`allow_headers`**: A list of HTTP headers allowed in the request.
  - Example: `["Authorization", "Content-Type"]`.
- **`allow_credentials`**: Whether to allow cookies or authentication headers in cross-origin requests.

### Allow `google.com` and `youtube.com`

```python
origins = [
    "https://www.google.com",
    "https://www.youtube.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Allow All Domains (Not Recommended for Production)

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Testing CORS Configuration

1. Update your FastAPI app with the CORS middleware.
2. Restart the FastAPI server.
3. Open a web browser and navigate to `google.com`.
4. Use the `fetch` API in the browser console to send a request to your API:

   ```javascript
   fetch('http://localhost:8000/')
     .then(res => res.json())
     .then(console.log);
   ```

5. If CORS is configured correctly, the request will succeed, and the response will be logged in the console. In this case, this was the output:

    ```javascript
    Promise { <state>: "pending" }
    <state>: "fulfilled"
    <value>: undefined
    <prototype>: Promise.prototype{ ... }
    Object { mesage: "Hello World" }
      message: "Hello World"
      <prototype>: Object { ... }
    ```

## Best Practices for CORS

1. **Restrict Allowed Origins**:
   - Only allow domains that need access to your API.
   - Avoid using `["*"]` in production.
2. **Limit HTTP Methods**:
   - Allow only the necessary HTTP methods (e.g., `GET` for read-only APIs).
3. **Use Secure Protocols**:
   - Always use `HTTPS` for allowed origins to ensure secure communication.
4. **Test Thoroughly**:
   - Test your CORS configuration with different domains and scenarios to ensure it works as expected.

## Common Issues and Fixes

### 1. **CORS Error Persists**

- **Cause**: The `allow_origins` list does not include the domain making the request.
- **Fix**: Add the domain to the `allow_origins` list.

### 2. **Credentials Not Sent**

- **Cause**: The `allow_credentials` parameter is not set to `True`.
- **Fix**: Set `allow_credentials=True` in the CORS middleware.

### 3. **Preflight Requests Failing**

- **Cause**: The server does not handle `OPTIONS` requests for preflight checks.
- **Fix**: Ensure `OPTIONS` is included in the `allow_methods` list.

[[TOC]]
