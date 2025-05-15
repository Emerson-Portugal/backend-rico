# produccion/models.py
from django.db import models

class Turno(models.Model):
    name = models.CharField(max_length=20, choices=[
            ('mañana', 'Mañana'),
            ('tarde', 'Tarde'),
            ('noche', 'Noche'),
        ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"
