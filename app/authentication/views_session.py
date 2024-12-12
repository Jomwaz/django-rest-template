from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from accounts.models import User
from accounts.serializers import UserSessionViewSetSerializer


class SessionLoginView(APIView):
    """View for session authentication. Login user."""

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"})
        else:
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class SessionLogoutView(APIView):
    """View for session authentication. Logout user."""

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})


# @authentication_classes([SessionAuthentication])
class SessionUserViewSet(APIView):
    """View for session authentication. Get user information."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return Response(
                {"message": "Invalid request."}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = UserSessionViewSetSerializer(user)
        return Response(data=serializer.data)
