# Authentication

Django provides its own authentication which should be the preferred route for handling authentication if the Django template system is how your application will go about implementing some type of frontend for the end-user (as you can simply feed the CSRF token and session ID through an index.html if using Django templates). If, however, you intend to pursue at least one of the below items,

1. Use a frontend framework running on a separate server.
2. Utilize Django simply as a backend API.

then the default authentication system I have laid out within the project template should be useful for getting you started quickly. 

## JSON Web Token

The authentication utilized for this Django backend template is JWT (JSON Web Token) authentication. The heavy lifting with regard to this setup is  completed with the [djoser](https://djoser.readthedocs.io/en/latest/index.html) library, but I have customized a few of the views so that the behavior of the endpoints more closely aligned with what I required more often than not (JWT authentication via cookies). 

The djoser documentation should be referred to if any attempts to extend or alter functionality beyond what I have scaffolded here is desired; as to what I have completed, continue reading to understand what has been made readily available. 

## Motivation
I wanted to be able to use Django's user account model for frontend application user authentication (and consequentially authentication for calling Django backend data to the frontend interface), but didn't want to use Django's template system for building a frontend application. 

JWT authentication allows for a unassociated frontend application to be built while also being able to leverage the powerful user model and user handling functionalities that Django offers out of the box.

## How It Works

How JWT authentication for this project template works is simple - 

- The user will supply their credentials to a "create JWT" endpoint. If the correct credentials are provided, the response will assign back an access and refresh token and, in this project's case specifically, they will be assigned as cookies in the user's browser.
 
  - NOTE: The access and refresh token have a defined lifetime for which they remain valid. 
          These lifetimes can be modified in the project settings. 

```python
# app/core/settings.py
AUTH_COOKIE_ACCESS_MAX_AGE = 60 * 60 # One hour
AUTH_COOKIE_REFRESH_MAX_AGE = 60 * 60 * 24 # One day
```

- A valid access token cookie can then be sent in subsequent requests to protected API endpoints on the Django backend to authenticate the user's permissions to access the endpoint/view and return a response.  

- The access token's lifetime is short, and to prevent the need for a user to continually require to supply credentials to generate a new valid access token after the token has expired, the longer lived refresh token can be used to generate a fresh access token without need for credentials being supplied.

- A "verify JWT" endpoint is used to periodically check the validity of the refresh token. If the refresh token is expired, the user can be, for example, automatically logged out the application.


## Endpoints

The djoser library provides a number of useful endpoints for customizing handling of authentication and other desired behavior in the realm of user accounts. As the purpose of the project template is to supply you with as quick of a start as possible, the five endpoints below are what I consider to be initially sufficient for most project cases.

```python
urlpatterns = [
    path("jwt/create/", CustomTokenObtainPairView.as_view()),
    path("jwt/refresh/", CustomTokenRefreshView.as_view()),
    path("jwt/verify/", CustomTokenVerifyView.as_view()),
    path("users/me/", CustomUserViewSet.as_view({"get": "me"})),
    path("logout/", LogoutView.as_view()),
]
```

## Usage
Assuming a user's account has already been created (either through an initial `createsuperuser` command, through the Django admin panel, or some other fashion built through the frontend) - a typical flow in a frontend application for how a user is authenticated is as follows,

1. `/jwt/create/` Supply credentials and get the access and refresh token.
```bash
# Request
curl --location 'localhost:8000/auth/jwt/create/' \
--header 'Content-Type: application/json' \
--header 'Cookie: access=eyJhbGciOi...; refresh=eyJhbGciOi....' \
--data '{
    "username": "johndoe",
    "password": "fake_password"
}'
# Successful response
{
    "access": "eyJhbGciOi...", 
    "refresh": "eyJhbGciOi..."
}
```

2. `/jwt/refresh/` Refresh access token (when required).
```bash
# Request
curl --location --request POST 'localhost:8000/auth/jwt/refresh/' \
--header 'Content-Type: application/json' \
--header 'Cookie: access=eyJhbGciOi...; refresh=eyJhbGciOi...'
# Successful response
{
    "access_token": "eyJhbGciO..."
}
```

3. `/jwt/verify/` Verify token validity (when required).
```bash
#Request
curl --location --request POST 'localhost:8000/auth/jwt/verify/' \
--header 'Content-Type: application/json' \
--header 'Cookie: access=eyJhbGciOi...; refresh=eyJhbGciOi...' \
--data ''
# Successful response
{} # No response data, but if token is valid, will receive a 200 OK status.
```

4. `/users/me` Get user information. Not necessary for the JWT authentication flow, but is very useful to have after the user is authenticated. (For example, a frontend application that first authenticates the user on login, and if successfully authenticated, makes a call to this endpoint to pull information on the user to display in an account settings page). 
```bash
# Request
curl --location 'localhost:8000/auth/users/me/' \
--header 'Cookie: access=eyJhbGciOi...; refresh=eyJhbGciOi...'
# Successful response
{
    "email": "john.doe@example_email_domain.com",
    "id": 1,
    "username": "johndoe"
}
```

5. `/logout/` Logout user. (Clears any access and refresh token cookies).
```bash
# Request
curl --location --request POST 'localhost:8000/auth/logout/'
# Successful response
{} # 204 NO CONTENT response.
```

## Final Remarks
For the sake of brevity, I have left out plenty with regard to JWT authentication, the djoser library, and the template code at large. For further knowledge of its workings, I, again, implore you to review the djoser library documentation, and to also review the `views.py` and `authentication.py` files within the authentication folder for a better understanding of the simple custom boilerplate authentication logic I have laid out. You will find that it should be easy to manipulate these views as needed to produce your desired behavior. 
