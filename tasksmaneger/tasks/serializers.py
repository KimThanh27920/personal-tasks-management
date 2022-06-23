from dataclasses import field
from rest_framework import serializers
from .models import Priority, Status,Task

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # exclude = ('workspace',)
        fields = '__all__'

class TaskReadSerializer(serializers.ModelSerializer):
    workspace = serializers.StringRelatedField()
    priority = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    class Meta:
        model = Task
        fields = '__all__'
        # exclude = ('workspace',)



