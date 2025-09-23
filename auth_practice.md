# SafeBoda Authentication Implementation Activity

**Duration:** 30-40 minutes | **Group Size:** 4 students per group

## Learning Objectives

By the end of this activity, you will:
- Implement a specific authentication method in Django REST Framework
- Understand the security implications of different authentication approaches
- Create and test authenticated API endpoints
- Compare authentication strategies with other groups

---

## Pre-Activity Setup

### Accept GitHub Classroom Assignment

1. Click on the assignment link provided by your instructor
2. Accept the assignment - this will create a fork of the safeboda repository
3. Clone your team's repository to your local machine
4. Create and activate a virtual environment
5. Install the existing requirements from requirements.txt
6. Run initial migrations and create a superuser for testing

### Determine Your Authentication Method

Your authentication method is based on your breakout room number:

- **Rooms 1, 4, 7, 10...** - Basic Authentication
- **Rooms 2, 5, 8, 11...** - Token Authentication
- **Rooms 3, 6, 9, 12...** - JWT Authentication

---

## Task Overview

You will implement a complete authentication system that includes:

1. Installing necessary packages
2. Configuring Django settings
3. Creating login/logout endpoints (where applicable)
4. Creating protected API endpoints
5. Testing your implementation
6. Documenting your approach

---

## Implementation Guide by Authentication Method

### ROOMS 1, 4, 7, 10... - Basic Authentication

**Key Resources:**
- DRF Authentication Documentation: https://www.django-rest-framework.org/api-guide/authentication/#basicauthentication
- DRF Tutorial on Authentication: https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/

**Implementation Steps:**

1. **Install Django REST Framework** if not already in requirements.txt

2. **Configure Authentication in settings.py**
   - Add rest_framework to INSTALLED_APPS
   - Configure REST_FRAMEWORK settings dictionary with BasicAuthentication
   - Set appropriate permission classes

3. **Create API Views**
   - Create at least two protected views in users/api_views.py:
     - User profile endpoint (returns current user information)
     - Riders list endpoint (returns all riders for passengers to view)
   - Use APIView or viewsets as appropriate
   - Apply permission classes to require authentication

4. **Configure URLs**
   - Add URL patterns in safeboda/urls.py or users/urls.py
   - Map your views to appropriate endpoints (e.g., /api/profile/, /api/riders/)

5. **Test Your Implementation**
   - Use curl, Postman, or Thunder Client
   - Test with valid credentials (email and password)
   - Test with invalid credentials
   - Verify authentication is required

**Security Considerations to Document:**
- Credentials sent with every request
- Base64 encoding (not encryption)
- HTTPS requirement
- Session management

---

### ROOMS 2, 5, 8, 11... - Token Authentication

**Key Resources:**
- DRF Token Authentication: https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
- Token Authentication Guide: https://www.django-rest-framework.org/api-guide/authentication/#setting-up-authentication

**Implementation Steps:**

1. **Install Dependencies**
   - Install Django REST Framework
   - Add rest_framework.authtoken to INSTALLED_APPS

2. **Configure Settings**
   - Add rest_framework to INSTALLED_APPS
   - Configure REST_FRAMEWORK with TokenAuthentication
   - Run migrations to create token table

3. **Create Authentication Endpoints**
   - Login view: accepts email/password, returns token
   - Logout view: deletes user's token
   - Use Django's authenticate() function
   - Use Token.objects.get_or_create() for token management

4. **Create Protected API Endpoints**
   - User profile endpoint
   - User-specific data endpoint (e.g., ride history or available riders)
   - Apply IsAuthenticated permission class

5. **Configure URL Routing**
   - Add paths for login, logout, and protected endpoints

6. **Test Implementation**
   - Obtain token via login endpoint
   - Use token in Authorization header: "Token YOUR_TOKEN_HERE"
   - Test token invalidation via logout

**Security Considerations to Document:**
- Token storage (database-backed)
- Token lifetime (does not expire by default)
- Token compromise scenarios
- Logout mechanism

---

### ROOMS 3, 6, 9, 12... - JWT Authentication

**Key Resources:**
- Simple JWT Documentation: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
- Getting Started: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
- DRF JWT Guide: https://www.django-rest-framework.org/api-guide/authentication/#json-web-token-authentication

**Implementation Steps:**

1. **Install Dependencies**
   - Install Django REST Framework
   - Install djangorestframework-simplejwt package

2. **Configure Settings**
   - Add rest_framework to INSTALLED_APPS
   - Configure REST_FRAMEWORK with JWTAuthentication
   - Configure SIMPLE_JWT settings (token lifetimes, algorithms)

3. **Create Authentication Views**
   - Custom login view that returns access and refresh tokens
   - Use RefreshToken.for_user() to generate tokens
   - Include token refresh endpoint using built-in TokenRefreshView

4. **Create Protected Endpoints**
   - User profile endpoint
   - Role-specific endpoint (e.g., rider-only or passenger-only view)
   - Ensure proper permission classes

5. **Configure URL Patterns**
   - Login endpoint
   - Token refresh endpoint
   - Protected API endpoints

6. **Test Your Implementation**
   - Login to receive access and refresh tokens
   - Use access token: "Bearer YOUR_ACCESS_TOKEN"
   - Test token refresh mechanism
   - Test token expiration

**Security Considerations to Document:**
- Stateless authentication
- Access vs refresh token purposes
- Token expiration and refresh strategy
- Signature verification

---

## Testing Requirements

Each group must demonstrate:

1. **Successful Authentication**
   - Show how a user authenticates
   - Display the authentication credentials/tokens

2. **Protected Endpoint Access**
   - Successfully access a protected endpoint
   - Show authentication header/credentials being used

3. **Authentication Failure**
   - Demonstrate what happens with invalid credentials
   - Show what happens when accessing protected endpoint without authentication

4. **Additional Functionality**
   - Logout (if applicable)
   - Token refresh (JWT only)

---

## Documentation Requirements

Create a README.md in your repository that includes:

### 1. Setup Instructions
- Additional packages installed
- Configuration changes made
- Migration commands run

### 2. API Endpoints
- List all endpoints created
- HTTP methods supported
- Authentication requirements
- Expected request/response formats

### 3. Authentication Flow
- Step-by-step process for authentication
- How to use credentials/tokens
- Token/session management approach

### 4. Testing Guide
- How to test each endpoint
- Sample requests (curl or similar)
- Expected responses

### 5. Security Analysis
- Key security features of your method
- Potential vulnerabilities
- Mitigation strategies
- When this method is appropriate to use

---

## Bonus Challenges

If you complete early, consider:

1. **Role-Based Access Control**: Implement different permissions for riders vs passengers
2. **Password Reset**: Add password reset functionality
3. **Rate Limiting**: Implement request throttling
4. **API Documentation**: Use DRF's browsable API or add OpenAPI/Swagger documentation
5. **Multi-Factor Authentication**: Research and outline how you would add 2FA

---

## Submission

1. **Code**: Push all changes to your GitHub Classroom repository
2. **Branch naming**: Use format `auth-[method]-implementation`
3. **Commit messages**: Use clear, descriptive commit messages
4. **README**: Include complete documentation in README.md

---

## Reflection Questions

After completing the activity, consider:

1. What are the main differences between stateful (Basic/Token) and stateless (JWT) authentication?
2. How does HTTPS factor into the security of each method?
3. Which method would you choose for:
   - A mobile application?
   - A microservices architecture?
   - A simple internal tool?
4. What additional security measures should be implemented regardless of authentication method?
5. How would you handle authentication in a production environment?
