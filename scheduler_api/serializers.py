from rest_framework import serializers
import scheduler_schema.models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserSchedulerCreate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)

    
class ScheduleDetailSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    class Meta:
        model = scheduler_schema.models.Schedule
        fields = '__all__'


class ScheduleCreateSerializer(serializers.ModelSerializer):
    # users = UserSchedulerCreate(many=True)

    class Meta:
        model = scheduler_schema.models.Schedule
        fields = '__all__'