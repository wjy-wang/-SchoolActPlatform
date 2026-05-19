from django.urls import path
from .views import (
    CommentListView,
    CommentCreateView,
    CommentDeleteView
)

urlpatterns = [
    path('activities/<int:activity_id>/comments/', CommentListView.as_view(), name='activity-comments'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
]
