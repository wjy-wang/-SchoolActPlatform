from django.urls import path
from apps.comments.views import ActivityCommentListView, CommentDeleteView

urlpatterns = [
    # 活动评论列表和发布评论
    path('activities/<int:activity_id>/comments/', ActivityCommentListView.as_view(), name='activity-comments'),
    # 删除评论
    path('comments/<int:comment_id>/', CommentDeleteView.as_view(), name='comment-delete'),
]
