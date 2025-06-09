# produccion/models.py
from django.db import models

from apps.produccion.utils.code_generator import generate_code
from core import settings

class Turno(models.Model):
    code = models.CharField(max_length=4, unique=True, editable=False, null=True)
    shift = models.CharField(max_length=20, choices=[
        ('MAÑANA', 'MAÑANA'),
        ('TARDE', 'TARDE'),
        ('NOCHE', 'NOCHE'),
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
        return f"{self.code} - {self.shift} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


# Se le asigana la fecha al turno de trabajo
class TurnoTrabajo(models.Model):
    code = models.CharField(max_length=4, unique=True, editable=False, null=True)

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
            while TurnoTrabajo.objects.filter(code=self.code).exists():
                self.code = generate_code()
        super().save(*args, **kwargs)




#aqui asigamos el turnoFecha a un usuario
class AsignacionTurno(models.Model):
    code = models.CharField(max_length=4, unique=True, editable=False, null=True)


    turno_trabajo = models.ForeignKey('produccion.TurnoTrabajo', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
            while AsignacionTurno.objects.filter(code=self.code).exists():
                self.code = generate_code()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('turno_trabajo', 'usuario')



