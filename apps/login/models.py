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
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=150)
