from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer, CommentCreateSerializer
from apps.comments.permissions import IsOwnerOrAdmin
from apps.activities.models import Activity


class ActivityCommentListView(APIView):
    """
    获取活动的评论列表或发布评论
    GET: 获取活动的评论列表（分页、按时间排序）
    POST: 发布评论
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)

        # 只获取未删除的评论
        comments = Comment.objects.filter(activity=activity, is_deleted=False).select_related('user')

        # 分页参数
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)

        try:
            page_size = int(page_size)
            if page_size <= 0 or page_size > 100:
                page_size = 10
        except (ValueError, TypeError):
            page_size = 10

        paginator = Paginator(comments, page_size)

        try:
            comments_page = paginator.page(page)
        except PageNotAnInteger:
            comments_page = paginator.page(1)
        except EmptyPage:
            comments_page = paginator.page(paginator.num_pages)

        serializer = CommentSerializer(comments_page, many=True)

        return Response({
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': comments_page.number,
            'page_size': page_size,
            'results': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)

        serializer = CommentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        comment = serializer.save(user=request.user, activity=activity)

        cache.delete(f"activity:detail:{activity_id}")

        response_serializer = CommentSerializer(comment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CommentDeleteView(APIView):
    """
    删除评论
    DELETE: 删除评论（普通用户只能删自己的，管理员可删任何）
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        # 检查权限（由 IsOwnerOrAdmin 权限类处理）
        self.check_object_permissions(request, comment)

        # 软删除：标记为已删除
        comment.is_deleted = True
        comment.save()

        # 清除相关缓存，确保数据一致性
        activity_id = comment.activity.id
        cache.delete(f"activity:detail:{activity_id}")

        return Response({
            'message': '评论删除成功'
        }, status=status.HTTP_200_OK)
