#prduccion/models/R145.py

from django.db import models

from apps.produccion.models import RegistroProduccionBase

# La R145-1 y R145-2 
class RegistroR145(RegistroProduccionBase):
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