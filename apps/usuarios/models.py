#models.py usuarios
from django.db import models
from django.contrib.auth.models import AbstractUser

class RolUsuario(models.TextChoices):
    OPERARIO = "OPERARIO", "Operario"
    REVISOR = "REVISOR", "Revisor"
    AUXILIAR = "AUXILIAR", "Auxiliar"
    SUPERVISOR = "SUPERVISOR", "Supervisor"

class Usuario(AbstractUser):
    rol = models.CharField(max_length=15, choices=RolUsuario.choices)
    codigo_interno = models.CharField(max_length=50, unique=True)
