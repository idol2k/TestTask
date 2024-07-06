from rest_framework import viewsets
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_client:
            serializer.save(client=self.request.user)
        else:
            serializer.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_employee:
            return Task.objects.filter(employee=user) | Task.objects.filter(employee__isnull=True)
        return Task.objects.filter(client=user)