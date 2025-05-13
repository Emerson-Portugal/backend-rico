# produccion/models.py
from django.db import models

class Maquina(models.Model):
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre

