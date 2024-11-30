from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthentication(JWTAuthentication):
    """
    Add to `authentication_classes()` decorator on view classes
    to enable JWT authentication.

    # Usage
    ```
    @authentication_classes([JWTAuthentication])
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
                raw_token = self.get_raw_token(header)

            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token

        except:
            return None
