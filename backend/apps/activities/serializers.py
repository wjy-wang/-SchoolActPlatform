from rest_framework import serializers
from .models import Activity
from apps.users.models import User


class ActivitySerializer(serializers.ModelSerializer):
    """活动序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    enrollment_count = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'description', 'type', 'start_time', 'end_time',
            'location', 'poster', 'organizer', 'status', 'created_by',
            'created_by_name', 'created_at', 'updated_at', 'enrollment_count',
            'is_enrolled', 'is_favorited'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_enrollment_count(self, obj):
        return obj.enrollments.count()

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.enrollments.filter(user=request.user).exists()
        return False

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False


class ActivityListSerializer(serializers.ModelSerializer):
    """活动列表序列化器（简化版）"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    enrollment_count = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'type', 'start_time', 'end_time',
            'location', 'poster', 'status', 'created_by_name',
            'created_at', 'enrollment_count'
        ]

    def get_enrollment_count(self, obj):
        return obj.enrollments.count()


class ActivityCreateSerializer(serializers.ModelSerializer):
    """创建活动序列化器"""
    poster = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Activity
        fields = [
            'title', 'description', 'type', 'start_time', 'end_time',
            'location', 'poster', 'organizer'
        ]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ActivityUpdateSerializer(serializers.ModelSerializer):
    """更新活动序列化器"""

    class Meta:
        model = Activity
        fields = [
            'title', 'description', 'type', 'start_time', 'end_time',
            'location', 'poster', 'organizer', 'status'
        ]
