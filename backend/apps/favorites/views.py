from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Favorite
from .serializers import FavoriteSerializer, FavoriteCreateSerializer
from apps.users.permissions import IsAdminUser


class FavoriteListView(generics.ListAPIView):
    """我的收藏列表"""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': '获取成功',
            'favorites': serializer.data,
            'count': queryset.count()
        })


class AllFavoriteListView(generics.ListAPIView):
    """所有收藏列表（仅管理员）"""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Favorite.objects.select_related('user', 'activity').order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': '获取成功',
            'favorites': serializer.data,
            'count': queryset.count()
        })


class FavoriteCreateView(generics.CreateAPIView):
    """收藏活动"""
    serializer_class = FavoriteCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        favorite = serializer.save()
        return Response({
            'message': '收藏成功',
            'favorite': FavoriteSerializer(favorite).data
        }, status=status.HTTP_201_CREATED)


class FavoriteDeleteView(generics.DestroyAPIView):
    """取消收藏"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': '取消收藏成功'
        }, status=status.HTTP_200_OK)
