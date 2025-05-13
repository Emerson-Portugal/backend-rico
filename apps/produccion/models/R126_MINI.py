
from django.db import models

from apps.produccion.models import RegistroProduccionBase


class RegistroR126Mini(RegistroProduccionBase):
    lote_anio = models.CharField(max_length=4)
    lote_sem = models.CharField(max_length=2)
    lote_dme = models.CharField(max_length=10)
    extension_dia = models.CharField(max_length=2)
    extension_dmp = models.CharField(max_length=10)
    extension_hora = models.TimeField()
    vencimiento = models.DateField()
    golpe = models.BooleanField(default=False)
    recor = models.BooleanField(default=False)
    Tinicial = models.DecimalField(max_length=10)
    vacio = models.BooleanField(default=False)
    dm = models.BooleanField(default=False)