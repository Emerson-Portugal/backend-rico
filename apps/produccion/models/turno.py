# produccion/models.py
from django.db import models

from apps.produccion.utils import generate_code

class Turno(models.Model):
    code = models.CharField(max_length=4, unique=True, editable=False, null=True)
    name = models.CharField(max_length=20, choices=[
        ('mañana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('noche', 'Noche'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
            while Turno.objects.filter(code=self.code).exists():
                self.code = generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"
