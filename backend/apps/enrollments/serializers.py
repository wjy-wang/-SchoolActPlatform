from rest_framework import serializers
from .models import Enrollment
from apps.activities.models import Activity
from apps.activities.serializers import ActivityListSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    activity = ActivityListSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'username', 'activity', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['activity']

    def validate_activity(self, value):
        if Enrollment.objects.filter(user=self.context['request'].user, activity=value).exists():
            raise serializers.ValidationError("您已经报过此活动了")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
