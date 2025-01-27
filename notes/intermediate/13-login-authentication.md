# JWT Token Authentication

## Introduction

JWT (JSON Web Token) is a method used for securely transmitting information between parties as a JSON object. It is a popular authentication mechanism due to its stateless nature, which makes it efficient for APIs and applications.

### Authentication Methods

There are two main ways to handle authentication:

1. **Session-based Authentication**:
   - The backend server stores session information to track user login status.
   - This session data can be stored in memory or a database.
   - When a user logs out, the session data is cleared.

2. **JWT-based Authentication**:
   - Stateless authentication method.
   - No session information is stored on the backend.
   - The authentication status is maintained via a token stored on the client side.

### Key Concept of JWT

- The JWT token is stored on the client side and is sent with every request.
- The server validates the token without maintaining a session, ensuring statelessness.

## JWT Authentication Flow

1. **Login**:
   - The client (frontend) sends a request to a `/login` endpoint with credentials (e.g., email and password).

2. **Credential Validation**:
   - The server verifies the provided credentials (e.g., matches the email and password).

3. **Token Creation**:
   - If valid, the server generates a JWT token.
   - The token is sent back to the client in the response.

4. **Accessing Resources**:
   - For subsequent requests (e.g., retrieving posts from `/posts`), the client includes the JWT token in the request header.
   - The server validates the token and, if valid, provides the requested data.

### Token Structure

- A JWT consists of three parts separated by dots (e.g., `header.payload.signature`)
- Here is a sample of an encoded JWT:

   ```plaintext
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
   ```

1. **Header**:
   - Contains metadata about the token, such as the signing algorithm (e.g., HS256) and the token type (e.g., JWT).
   - From the sample above, here is the decoded header:

     ```json
     {
       "alg": "HS256",
       "typ": "JWT"
     }
     ```

2. **Payload**:
   - Contains the data (claims) to be shared.
   - Example claims:
     - User ID
     - User role (e.g., admin, regular user)
   - Note: The payload is not encrypted, so sensitive information should not be included.
   - From the sample above, here is the decoded payload:

   ```plaintext
   {
      "sub": "1234567890",    -- subject
      "name": "John Doe",
      "iat": 1516239022       -- issued at
   }
   ```

3. **Signature**:
   - Ensures the integrity of the token.
   - Created by hashing the header, payload, and a secret key.
   - Only the server knows the secret key, ensuring that tampered tokens can be identified.
   - Here is the decoded signature from the above JWT:

   ```plaintext
   HMACSHA256(
      base64UrlEncode(header) + "." +
      base64UrlEncode(payload),
      your-256-bit-secret
   ) secret base64 encoded
   ```

### Purpose of the Signature

- The signature ensures **data integrity**, confirming that no one has tampered with the token.
- If the token is altered (e.g., changing the user role), the signature will no longer match, and the server will reject it.

### Validation Process

1. The server extracts the header, payload, and signature from the token.
2. It recreates the signature using the header, payload, and its secret key.
3. The server compares the recreated signature with the one in the token.
   - If they match, the token is valid.
   - If they don’t match, the token is rejected.

## Key Points to Remember

- **Stateless**: JWT authentication does not store session information on the server.
- **Not Encrypted**: The payload is visible and should not contain sensitive information.
- **Signature Integrity**: The signature ensures that the token has not been tampered with.
- **Efficient**: Suitable for APIs as it reduces server-side load.

## Best Practices

1. **Keep Secrets Secure**:
   - The secret key should only be accessible to the server.

2. **Minimal Payload**:
   - Include only essential information in the payload to reduce token size and avoid bandwidth wastage.

3. **Use HTTPS**:
   - Always use HTTPS to prevent token interception.

4. **Token Expiry**:
   - Set an expiration time for tokens to enhance security.

5. **Refresh Tokens**:
   - Use refresh tokens to generate new tokens without requiring a full login.

## Testing JWT Tokens

1. Obtain an access token from `/login` (created in the next section)
2. Copy the token and paste it into [jwt.io](https://jwt.io/) to decode.
3. The decoded token should contain the user ID and expiration time.

[[TOC]]
