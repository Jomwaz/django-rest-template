from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """User serializier with all fields."""

    class Meta:
        model = User
        fields = "__all__"


class UserSessionViewSetSerializer(serializers.ModelSerializer):
    """User serializer for sending general user information without compromisable user authentication information.

    ## Fields
        `id, last_login, username, email, first_name, last_name`

    """

    class Meta:
        model = User
        fields = ("id", "last_login", "username", "email", "first_name", "last_name")
