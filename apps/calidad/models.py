#models.py calidad
from django.db import models
from apps.produccion.models import RegistroProduccion
from apps.usuarios.models import Usuario, RolUsuario

class RegistroOperario(models.Model):
    registro = models.OneToOneField(RegistroProduccion, on_delete=models.CASCADE)
    operario = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': RolUsuario.OPERARIO})

class RegistroRevisor(models.Model):
    registro = models.OneToOneField(RegistroProduccion, on_delete=models.CASCADE)
    revisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': RolUsuario.REVISOR})
    observacion = models.TextField(blank=True)

class RegistroAuxiliar(models.Model):
    registro = models.OneToOneField(RegistroProduccion, on_delete=models.CASCADE)
    auxiliar = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': RolUsuario.AUXILIAR})
    observacion = models.TextField(blank=True)
