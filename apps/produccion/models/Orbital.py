
from django.db import models

from apps.produccion.models import RegistroProduccionBase


class RegistroOrbital(RegistroProduccionBase):
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    lote = models.CharField(max_length=10)
    Tinicial = models.DecimalField(max_length=10)
    veloc = models.BooleanField(default=False)
