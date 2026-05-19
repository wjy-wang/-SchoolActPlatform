from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_role = serializers.IntegerField(source='user.role', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'username', 'user_role', 'activity', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['activity', 'content']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
