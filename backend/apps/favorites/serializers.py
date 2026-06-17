from rest_framework import serializers
from .models import Favorite
from apps.activities.serializers import ActivityListSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    activity = ActivityListSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    student_id = serializers.CharField(source='user.student_id', read_only=True)
    activity_title = serializers.CharField(source='activity.title', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'username', 'student_id', 'activity', 'activity_title', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['activity']

    def validate_activity(self, value):
        if Favorite.objects.filter(user=self.context['request'].user, activity=value).exists():
            raise serializers.ValidationError("您已经收藏过此活动了")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
