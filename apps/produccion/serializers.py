# produccion/serializers.py

from rest_framework import serializers
from .models import Producto, Maquina, Turno

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'code', 'name']

class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = ['id', 'code', 'name']

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ['id', 'code', 'name', 'start_time', 'end_time']
