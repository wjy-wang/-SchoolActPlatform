from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    自定义权限：
    - 普通用户只能删除自己的评论
    - 管理员可以删除任何评论
    """
    def has_object_permission(self, request, view, obj):
        # 管理员有所有权限
        if request.user.role == 1:
            return True
        # 普通用户只能操作自己的资源
        return obj.user == request.user
