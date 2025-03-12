from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmation_code = models.CharField(max_length=4, blank=True)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_users",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_users",
        blank=True,
    )

    def __str__(self):
        return f"{self.name} {self.surname}"
