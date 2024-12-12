from django.urls import path
from .views_jwt import (
    JwtTokenObtainPairView,
    JwtTokenRefreshView,
    JwtTokenVerifyView,
    JwtLogoutView,
    JwtUserViewSet,
)
from .views_session import (
    SessionLoginView,
    SessionLogoutView,
    SessionUserViewSet,
)

urlpatterns = [
    path("jwt/create/", JwtTokenObtainPairView.as_view()),
    path("jwt/refresh/", JwtTokenRefreshView.as_view()),
    path("jwt/verify/", JwtTokenVerifyView.as_view()),
    path("jwt/logout/", JwtLogoutView.as_view()),
    path("session/create/", SessionLoginView.as_view()),
    path("session/logout/", SessionLogoutView.as_view()),
    path("session/user/", SessionUserViewSet.as_view()),
    path("users/me/", JwtUserViewSet.as_view({"get": "me"})),
]
