# produccion/models.py
from django.db import models

from apps.produccion.utils import generate_code

class Maquina(models.Model):
    code = models.CharField(max_length=4, unique=True, editable=False, null=True)
    name = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
            # Asegura unicidad
            while Maquina.objects.filter(code=self.code).exists():
                self.code = generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"

