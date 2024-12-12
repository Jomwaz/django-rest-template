from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """JWT authentication looking for a cookie.

    Modified from the base JWTAuthentication class to instead
    pull the access token value from a cookie rather than
    an authentication header.

    Add to `authentication_classes()` decorator on view classes
    to enable JWT authentication.

    # Usage

    ```
    @authentication_classes([CookieJWTAuthentication])
    class SomeView(generics.ListCreateAPIView):
        # Add view code below...
    ```
    """

    def authenticate(self, request):
        try:
            header = self.get_header(request)
            if header is None:
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
            else:
                return None

            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token

        except:
            return None
