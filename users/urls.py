from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import RegisterView, CreateProfileView, ChangePasswordView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('create-profile/', CreateProfileView.as_view(), name='create-profile'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("change-password/", ChangePasswordView.as_view())
]