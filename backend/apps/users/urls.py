from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
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
    # 认证相关
    path('auth/register/', UserRegisterView.as_view(), name='user-register'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/logout/', logout_view, name='user-logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # 用户个人信息
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
    path('auth/password/', PasswordChangeView.as_view(), name='password-change'),
    
    # 用户管理（管理员）
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
