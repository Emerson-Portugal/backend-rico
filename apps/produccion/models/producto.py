# produccion/models.py
from django.db import models

class Producto(models.Model):
    code  = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    day = models.IntegerField(default=0, null=True)
    type = models.CharField(max_length=20, choices=[
        ('CRUDO', 'CRUDO'),
        ('COCIDO', 'COCIDO')
    ])

    def __str__(self):
        return f"{self.code} - {self.name} - {self.day}- {self.type}"

