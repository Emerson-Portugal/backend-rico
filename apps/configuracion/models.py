#models.py configuracion
from django.db import models

class TipoTurno(models.TextChoices):
    MANANA = "MAN", "Mañana"
    TARDE = "TAR", "Tarde"
    NOCHE = "NOC", "Noche"

class TipoMaquina(models.TextChoices):
    R145 = "R145", "R145"
    R126 = "R126", "R126"

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Turno(models.Model):
    fecha = models.DateField()
    tipo = models.CharField(max_length=3, choices=TipoTurno.choices)

class Maquina(models.Model):
    tipo = models.CharField(max_length=10, choices=TipoMaquina.choices)
