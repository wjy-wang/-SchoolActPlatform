from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Enrollment
from .serializers import EnrollmentSerializer, EnrollmentCreateSerializer
from apps.activities.models import Activity
from apps.users.permissions import IsAdminUser


class EnrollmentListView(generics.ListAPIView):
    """我的报名列表"""
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': '获取成功',
            'enrollments': serializer.data,
            'count': queryset.count()
        })


class AllEnrollmentListView(generics.ListAPIView):
    """所有报名列表（仅管理员）"""
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Enrollment.objects.select_related('user', 'activity').order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': '获取成功',
            'enrollments': serializer.data,
            'count': queryset.count()
        })


class ActivityEnrollmentListView(generics.ListAPIView):
    """活动的报名列表（仅管理员）"""
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        activity_id = self.kwargs.get('activity_id')
        return Enrollment.objects.filter(activity_id=activity_id).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': '获取成功',
            'enrollments': serializer.data,
            'count': queryset.count()
        })


class EnrollmentCreateView(generics.CreateAPIView):
    """报名活动"""
    serializer_class = EnrollmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save()
        return Response({
            'message': '报名成功',
            'enrollment': EnrollmentSerializer(enrollment).data
        }, status=status.HTTP_201_CREATED)


class EnrollmentDeleteView(generics.DestroyAPIView):
    """取消报名"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': '取消报名成功'
        }, status=status.HTTP_200_OK)
