from rest_framework import serializers
from .models import User, Task, Client


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "is_employee", "is_client"]

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "employee", "report", "created_by"]

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            if request.user.is_client:
                client = Client.objects.get(user=request.user)
                return Task.objects.create(created_by=client, **validated_data)
            else:
                raise serializers.ValidationError("Only clients can create tasks.")
        raise serializers.ValidationError("Request context is not available.")

    def update(self, instance, validated_data):
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            if request.user.is_employee:
                instance.status = validated_data.get("status", instance.status)
                instance.report = validated_data.get("report", instance.report)
                instance.save()
                return instance
            else:
                raise serializers.ValidationError("Only employees can update tasks.")
        raise serializers.ValidationError("Request context is not available.")
