
from django.db import models

from apps.produccion.models import RegistroProduccionBase


class RegistroPuma(RegistroProduccionBase):
    lote = models.CharField(max_length=10)
    stickers = models.CharField(max_length=10)
    Tinicial = models.DecimalField(max_length=10)
    recor = models.BooleanField(default=False)
