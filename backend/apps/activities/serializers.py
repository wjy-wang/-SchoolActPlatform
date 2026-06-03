from rest_framework import serializers
from .models import Activity
from apps.users.models import User


class ActivitySerializer(serializers.ModelSerializer):
    """活动序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    enrollment_count = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'description', 'type', 'start_time', 'end_time',
            'location', 'poster', 'organizer', 'status', 'created_by',
            'created_by_name', 'created_at', 'updated_at', 'enrollment_count',
            'is_enrolled', 'is_favorited', 'can_edit', 'can_delete'
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

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # 管理员可以编辑所有活动，创建者可以编辑自己的活动
            return request.user.role == 1 or obj.created_by.id == request.user.id
        return False

    def get_can_delete(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # 管理员可以删除所有活动，创建者可以删除自己的活动
            return request.user.role == 1 or obj.created_by.id == request.user.id
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
    poster = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Activity
        fields = [
            'title', 'description', 'type', 'start_time', 'end_time',
            'location', 'poster', 'organizer', 'status'
        ]
        read_only_fields = ['created_by']

    def validate(self, data):
        """验证数据"""
        # 检查开始时间和结束时间
        if 'start_time' in data and 'end_time' in data:
            if data['start_time'] >= data['end_time']:
                raise serializers.ValidationError('开始时间必须早于结束时间')
        elif 'start_time' in data:
            instance = self.instance
            if data['start_time'] >= instance.end_time:
                raise serializers.ValidationError('开始时间必须早于结束时间')
        elif 'end_time' in data:
            instance = self.instance
            if data['end_time'] <= instance.start_time:
                raise serializers.ValidationError('结束时间必须晚于开始时间')
        
        # 检查状态转换是否合法
        if 'status' in data:
            instance = self.instance
            current_status = instance.status if instance else 0
            new_status = data['status']
            
            # 状态转换规则：未开始(0) → 进行中(1) → 已结束(2)
            status_transitions = {
                0: [0, 1],      # 未开始可以变为未开始或进行中
                1: [1, 2],      # 进行中可以变为进行中或已结束
                2: [2]           # 已结束只能保持已结束
            }
            
            if new_status not in status_transitions.get(current_status, []):
                raise serializers.ValidationError(f'状态转换不合法：从{current_status}到{new_status}')
        
        return data
