#prduccion/models/R145.py

from django.db import models

from apps.produccion.models import RegistroProduccionBase
from core import settings
from apps.produccion.utils.code_generator import generate_code


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


    lote_anio = models.CharField(max_length=4, blank=True, null=True)
    lote_sem = models.CharField(max_length=2, blank=True, null=True)
    lote_dme = models.CharField(max_length=10, blank=True, null=True)

    extension_dia = models.CharField(max_length=2, blank=True, null=True)
    extension_dmp = models.CharField(max_length=10, blank=True, null=True)
    extension_hora = models.TimeField(blank=True, null=True)
    vencimiento = models.DateField(blank=True, null=True)
    
    golpe = models.IntegerField(default=0, null=True)
    recor = models.CharField(max_length=10, blank=True, null=True)

    peso = models.CharField(max_length=10, blank=True, null=True)
    vacio = models.CharField(max_length=10, blank=True, null=True)
    dm = models.CharField(max_length=10, blank=True, null=True)



   # Fases
    operario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='operarios', on_delete=models.CASCADE)
    revisador = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='revisadores', null=True, blank=True, on_delete=models.SET_NULL)
    auxiliar = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='auxiliares', null=True, blank=True, on_delete=models.SET_NULL)

    fecha_operario = models.DateTimeField(auto_now_add=True)
    fecha_revisador = models.DateTimeField(null=True, blank=True)
    fecha_auxiliar = models.DateTimeField(null=True, blank=True)

