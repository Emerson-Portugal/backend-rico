#models.py produccion
from django.db import models
from apps.configuracion.models import Producto, Turno, Maquina
from apps.usuarios.models import Usuario

class EstadoRegistro(models.TextChoices):
    REGISTRADO = "REG", "Registrado"
    REVISADO = "REV", "Revisado"
    VALIDADO_DM = "DM", "Validado por D.M."
    FINALIZADO = "FIN", "Finalizado"
    OBSERVADO = "OBS", "Observado"

class RegistroProduccion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    unidades = models.IntegerField()
    lote = models.CharField(max_length=50)
    dia_codificado = models.IntegerField()
    dia_mes_empaque = models.CharField(max_length=10)
    dia_mes_produccion = models.CharField(max_length=10)
    hora_produccion = models.CharField(max_length=10)
    extension = models.CharField(max_length=20)
    vencimiento = models.DateField()
    golpe = models.IntegerField()
    recorte = models.FloatField()

    peso_verificado = models.BooleanField(default=False)
    vacio_verificado = models.BooleanField(default=False)
    detector_metales_check = models.BooleanField(default=False)

    estado = models.CharField(max_length=10, choices=EstadoRegistro.choices, default=EstadoRegistro.REGISTRADO)

    tipo_turno = models.ForeignKey(Turno, on_delete=models.SET_NULL, null=True)
    tipo_maquina = models.ForeignKey(Maquina, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.producto.codigo} - {self.fecha} - {self.estado}"
