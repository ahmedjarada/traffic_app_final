from datetime import timedelta

from django.db import models
from django.utils import timezone

from user.models import User as SuperUser


class ClientToken(models.Model):
    token = models.TextField(null=False, max_length=254, default="NAN")
    is_alive = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_created=True, default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())
    expired_at = models.DateTimeField(default=timezone.now() + timedelta(hours=10))
    user_id = models.ForeignKey(SuperUser, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.id}, {self.token}"


class ClientVerificationCode(models.Model):
    PIN = models.TextField(null=False, max_length=254, default="NAN")
    createdAt = models.DateTimeField(auto_created=True, default=timezone.now())
    is_opened = models.BooleanField(default=False)
    reset_by = models.CharField(choices=(('E', 'Email'), ('M', 'Mobile')), default=None, max_length=1)
    user_id = models.ForeignKey(SuperUser, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.id}, {self.PIN}"


class ClientResetCode(models.Model):
    code = models.PositiveIntegerField(default=0, null=False)
    createdAt = models.DateTimeField(auto_created=True, default=timezone.now())
    is_opened = models.BooleanField(default=False)
    reset_for = models.CharField(choices=(('E', 'Email'), ('P', 'Password')), default=None, max_length=1)
    user_id = models.ForeignKey(SuperUser, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.id}, {self.code}"
