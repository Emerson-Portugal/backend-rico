#prduccion/models/R145.py

from django.db import models

from apps.produccion.models import RegistroProduccionBase
from core import settings
from apps.produccion.utils import generate_code


# La R145-1 y R145-2 
class RegistroR145(RegistroProduccionBase):

    code = models.CharField(max_length=4, unique=True, editable=False, null=True)


    def save(self, *args, **kwargs):
            if not self.code:
                self.code = generate_code()
                # Asegura unicidad
                while RegistroR145.objects.filter(code=self.code).exists():
                    self.code = generate_code()
            super().save(*args, **kwargs)


    lote_anio = models.CharField(max_length=4)
    lote_sem = models.CharField(max_length=2)
    lote_dme = models.CharField(max_length=10)
    extension_dia = models.CharField(max_length=2)
    extension_dmp = models.CharField(max_length=10)
    extension_hora = models.TimeField()
    vencimiento = models.DateField()
    golpe = models.BooleanField(default=False)
    recor = models.BooleanField(default=False)
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    vacio = models.BooleanField(default=False)
    dm = models.BooleanField(default=False)


   # Fases
    operario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='operarios', on_delete=models.CASCADE)
    revisador = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='revisadores', null=True, blank=True, on_delete=models.SET_NULL)
    auxiliar = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='auxiliares', null=True, blank=True, on_delete=models.SET_NULL)

    fecha_operario = models.DateTimeField(auto_now_add=True)
    fecha_revisador = models.DateTimeField(null=True, blank=True)
    fecha_auxiliar = models.DateTimeField(null=True, blank=True)

