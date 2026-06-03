from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .models import Activity
from .serializers import (
    ActivitySerializer,
    ActivityListSerializer,
    ActivityCreateSerializer,
    ActivityUpdateSerializer
)
from apps.users.permissions import IsAdminUser, IsActivityOwnerOrAdmin
from apps.comments.models import Comment


class ActivityListView(generics.ListAPIView):
    """活动列表视图"""
    serializer_class = ActivityListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Activity.objects.all().order_by('-created_at')
        activity_type = self.request.query_params.get('type', None)
        status_filter = self.request.query_params.get('status', None)

        if activity_type is not None:
            queryset = queryset.filter(type=activity_type)
        if status_filter is not None:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': '获取成功',
            'activities': serializer.data,
            'count': queryset.count()
        })


class ActivityDetailView(generics.RetrieveAPIView):
    """活动详情视图（带缓存，评论列表请调用独立接口）"""
    serializer_class = ActivitySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Activity.objects.select_related('created_by')

    def retrieve(self, request, *args, **kwargs):
        activity_id = self.kwargs.get('pk')
        cache_key = f"activity:detail:{activity_id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response({
                'message': '获取成功（缓存）',
                **cached_data
            })

        instance = self.get_object()
        comment_count = Comment.objects.filter(
            activity=instance,
            is_deleted=False
        ).count()  # count() 只返回数量，无需 select_related

        activity_serializer = self.get_serializer(instance, context={'request': request})

        data = {
            'activity': activity_serializer.data,
            'comment_count': comment_count
        }

        cache.set(cache_key, data, timeout=300)

        return Response({
            'message': '获取成功',
            **data
        })


class ActivityCreateView(generics.CreateAPIView):
    """创建活动视图（仅管理员）"""
    serializer_class = ActivityCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activity = serializer.save()
        return Response({
            'message': '活动创建成功',
            'activity': ActivitySerializer(activity, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)


class ActivityUpdateView(generics.UpdateAPIView):
    """更新活动视图（活动创建者或管理员）"""
    serializer_class = ActivityUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsActivityOwnerOrAdmin]
    queryset = Activity.objects.select_related('created_by')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        activity = serializer.save()
        
        cache.delete(f"activity:detail:{activity.pk}")
        
        return Response({
            'message': '活动更新成功',
            'activity': ActivitySerializer(activity, context={'request': request}).data
        }, status=status.HTTP_200_OK)


class ActivityDeleteView(generics.DestroyAPIView):
    """删除活动视图（仅管理员）"""
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    queryset = Activity.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cache.delete(f"activity:detail:{instance.pk}")
        self.perform_destroy(instance)
        return Response({
            'message': '活动删除成功'
        }, status=status.HTTP_200_OK)


class ActivityBulkUpdateView(APIView):
    """批量更新活动状态（仅管理员）"""
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def patch(self, request):
        """批量更新活动状态"""
        activity_ids = request.data.get('activity_ids', [])
        status_data = request.data.get('status')
        
        if not activity_ids or status_data is None:
            return Response({
                'error': '缺少必要参数：activity_ids 和 status'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新活动状态
        updated_count = Activity.objects.filter(
            id__in=activity_ids
        ).update(status=status_data)
        
        # 清除相关缓存
        for activity_id in activity_ids:
            cache.delete(f"activity:detail:{activity_id}")
        
        return Response({
            'message': f'成功更新 {updated_count} 条活动',
            'updated_count': updated_count
        }, status=status.HTTP_200_OK)


class MyActivitiesView(generics.ListAPIView):
    """我的活动列表（管理员创建的活动）"""
    serializer_class = ActivityListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(created_by=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': '获取成功',
            'activities': serializer.data,
            'count': queryset.count()
        })
