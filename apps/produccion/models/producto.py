# produccion/models.py
from django.db import models

class Producto(models.Model):
    code  = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.code} - {self.name}"

