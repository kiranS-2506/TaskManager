from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    owner = serializers.CharField(source="owner.username", read_only=True)
    due_date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Task
        fields = [
            "id", 
            "owner",
            "title",
            "description",
            "status",
            "created_at",
            "due_date"
            ]