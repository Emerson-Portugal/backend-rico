# produccion/models.py
from django.db import models

class Turno(models.Model):
    nombre = models.CharField(max_length=20, choices=[
            ('mañana', 'Mañana'),
            ('tarde', 'Tarde'),
            ('noche', 'Noche'),
        ])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.nombre} ({self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')})"
