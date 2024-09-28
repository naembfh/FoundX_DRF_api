from django.urls import path
from .views import UserRegisterView, UserLoginView, ChangePasswordView, RefreshTokenView, GetAllUsersView, GetSingleUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # User Management Routes
    path('create-user/', UserRegisterView.as_view(), name='create-user'),
    path('users/', GetAllUsersView.as_view(), name='get-all-users'),
    path('users/<int:id>/', GetSingleUserView.as_view(), name='get-single-user'),
    
    path('login/', UserLoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
]
