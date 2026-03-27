from rest_framework import serializers
from .models import Report, Ban

class ReportSerializer(serializers.ModelSerializer):
    reporter_username = serializers.CharField(source='reporter.username', read_only=True)
    reported_user_username = serializers.CharField(source='reported_user.username', read_only=True)
    
    class Meta:
        model = Report
        fields = ['id', 'reporter', 'reporter_username', 'reported_user', 'reported_user_username', 
                  'content_type', 'object_id', 'reason', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class BanSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    moderator_username = serializers.CharField(source='moderator.username', read_only=True)
    
    class Meta:
        model = Ban
        fields = ['id', 'user', 'user_username', 'moderator', 'moderator_username', 
                  'reason', 'duration_days', 'is_active', 'expires_at', 'created_at']
        read_only_fields = ['id', 'created_at', 'expires_at', 'is_active']
