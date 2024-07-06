from rest_framework import viewsets
from .models import User, Task, Employee, Client
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

    def get_queryset(self):
        user = self.request.user
        if user.is_employee:
            employee = Employee.objects.get(user=user)
            return Task.objects.filter(employee=employee) | Task.objects.filter(employee=None)
        elif user.is_client:
            client = Client.objects.get(user=user)
            return Task.objects.filter(created_by=client)
        return Task.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_client:
            client = Client.objects.get(user=user)
            serializer.save(created_by=client)
        else:
            raise PermissionError("Only clients can create tasks.")

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_employee:
            serializer.save()
        else:
            raise PermissionError("Only employees can update tasks.")