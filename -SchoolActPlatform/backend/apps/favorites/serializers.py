from rest_framework import serializers
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    activity_title = serializers.CharField(source='activity.title', read_only=True)
    activity_type = serializers.IntegerField(source='activity.type', read_only=True)
    activity_start_time = serializers.DateTimeField(source='activity.start_time', read_only=True)
    activity_location = serializers.CharField(source='activity.location', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'username', 'activity', 'activity_title', 'activity_type',
                  'activity_start_time', 'activity_location', 'created_at']
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
