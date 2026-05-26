from rest_framework import serializers
from apps.comments.models import Comment
from apps.users.models import User


class CommentUserSerializer(serializers.ModelSerializer):
    """评论用户信息序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'student_id']


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    user = CommentUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'activity', 'content', 'created_at', 'is_deleted']
        read_only_fields = ['id', 'user', 'created_at', 'is_deleted']


class CommentCreateSerializer(serializers.ModelSerializer):
    """创建评论序列化器"""
    class Meta:
        model = Comment
        fields = ['content']

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("评论内容不能为空")
        if len(value) > 500:
            raise serializers.ValidationError("评论内容不能超过500字符")
        return value.strip()
