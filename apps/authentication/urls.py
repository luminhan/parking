from django.urls import include, path
from rest_framework_simplejwt import views

urlpatterns = [
    path("", include("djoser.urls")),
    # Route for login
    path("jwt/create/", views.TokenObtainPairView.as_view(), name="jwt-create"),
    # Route for refreshing the token
    path("jwt/refresh/", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    # Route to verify the integrity of the token
    path("jwt/verify/", views.TokenVerifyView.as_view(), name="jwt-verify"),
]
