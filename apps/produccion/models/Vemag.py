
from django.db import models

from apps.produccion.models import RegistroProduccionBase


class RegistroVenag(RegistroProduccionBase):
    stickers = models.CharField(max_length=10)
    lote = models.CharField(max_length=10)
    Tinicial = models.DecimalField(max_length=10)
