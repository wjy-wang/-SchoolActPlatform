from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserProfileView,
    PasswordChangeView,
    UserListView,
    UserDetailView,
    logout_view
)

urlpatterns = [
    path('auth/register/', UserRegisterView.as_view(), name='user-register'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/logout/', logout_view, name='user-logout'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
    path('auth/password/', PasswordChangeView.as_view(), name='password-change'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
