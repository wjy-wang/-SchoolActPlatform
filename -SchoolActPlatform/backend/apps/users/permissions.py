from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """检查用户是否为管理员（is_staff=True）"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """检查用户是否为资源所有者或管理员"""
    def has_object_permission(self, request, view, obj):
        # 管理员有所有权限
        if request.user.is_staff:
            return True
        # 用户只能访问自己的资源
        return obj.id == request.user.id


class IsRegularUser(permissions.BasePermission):
    """检查用户是否为普通用户（非管理员）"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_staff


class IsActivityOwnerOrAdmin(permissions.BasePermission):
    """检查用户是否为活动创建者或管理员"""
    def has_object_permission(self, request, view, obj):
        # 管理员有所有权限
        if request.user.is_staff:
            return True
        # 用户只能编辑自己创建的活动
        return obj.created_by.id == request.user.id
