from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает исполнителя'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнена'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    client = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    employee = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    report = models.TextField(blank=True)

    def __str__(self):
        return self.title