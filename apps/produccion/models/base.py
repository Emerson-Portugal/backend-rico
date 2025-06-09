# produccion/models.py
from django.db import models

from apps.produccion.models import Producto, Maquina, Turno


class RegistroProduccionBase(models.Model):
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    maquina = models.TextField(blank=True)
    turno = models.TextField(blank=True)

    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    unidad_kilos = models.DecimalField(max_digits=10, decimal_places=2, null=True)





    estado = models.CharField(max_length=20, choices=[
        ('PENDIENTE', 'PENDIENTE'),
        ('EN_PROCESO', 'EN_PROCESO'),
        ('FINALIZADO', 'FINALIZADO'),
    ], default='PENDIENTE')


    fase = models.CharField(max_length=20, choices=[
        ('OPERARIO', 'OPERARIO'),
        ('REVISADOR', 'REVISADOR'),
        ('AUXILIAR', 'AUXILIAR'),
        ('FINALIZADO', 'FINALIZADO'),
    ], default='OPERARIO')


    observaciones = models.TextField(blank=True)

    class Meta:
        abstract = True