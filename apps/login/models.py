from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'ADMIN'),
        ('REVISADOR', 'REVISADOR'),
        ('AUXILIAR', 'AUXILIAR'),
        ('SUPERVISOR', 'SUPERVISOR'),
        ('OPERADOR', 'OPERADOR'),
    ]

    username = None  # Eliminamos username
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']
