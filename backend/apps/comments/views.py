from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from apps.users.permissions import IsAdminUser


class CommentListView(generics.ListAPIView):
    """活动的评论列表"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        activity_id = self.kwargs.get('activity_id')
        return Comment.objects.filter(activity_id=activity_id).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': '获取成功',
            'comments': serializer.data,
            'count': queryset.count()
        })


class CommentCreateView(generics.CreateAPIView):
    """发表评论"""
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response({
            'message': '评论成功',
            'comment': CommentSerializer(comment).data
        }, status=status.HTTP_201_CREATED)


class CommentDeleteView(generics.DestroyAPIView):
    """删除评论（仅管理员或评论者本人）"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 1:
            return Comment.objects.all()
        return Comment.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': '删除成功'
        }, status=status.HTTP_200_OK)
