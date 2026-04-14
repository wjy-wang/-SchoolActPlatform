from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .serializers import (
    UserSerializer, 
    UserRegisterSerializer, 
    UserLoginSerializer,
    UserProfileUpdateSerializer,
    PasswordChangeSerializer
)
from .permissions import IsAdminUser, IsOwnerOrAdmin

User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    """用户注册视图"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': '注册成功',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class UserLoginView(TokenObtainPairView):
    """用户登录视图（JWT Token）"""
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 获取token数据
        data = serializer.validated_data
        
        # 如果请求中包含 remember_me 参数，延长token过期时间
        remember_me = request.data.get('remember_me', False)
        if remember_me:
            # 延长refresh token的有效期到7天
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(serializer.user)
            refresh.set_exp(lifetime=timedelta(days=7))
            data['refresh'] = str(refresh)
        
        return Response({
            'message': '登录成功',
            'access': data['access'],
            'refresh': data['refresh'],
            'user': {
                'id': serializer.user.id,
                'username': serializer.user.username,
                'role': serializer.user.role,
                'student_id': serializer.user.student_id,
            }
        })


class UserProfileView(generics.RetrieveUpdateAPIView):
    """用户个人信息视图"""
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response({
            'message': '获取成功',
            'user': serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': '更新成功',
            'user': UserSerializer(instance).data
        })


class PasswordChangeView(generics.UpdateAPIView):
    """密码修改视图"""
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = self.get_object()
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': '密码修改成功'
        }, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    """用户列表视图（仅管理员）"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """用户详情视图（管理员或本人）"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """用户登出视图"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            from rest_framework_simplejwt.tokens import RefreshToken
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': '登出成功'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': '登出失败', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
