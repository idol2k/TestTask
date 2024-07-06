from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def save(self, *args, **kwargs):
        if self.is_client and self.is_employee:
            raise ValueError("User cannot be both client and employee.")
        super().save(*args, **kwargs)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Access(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_view_all_tasks = models.BooleanField(default=False)


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    report = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.title