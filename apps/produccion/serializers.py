# produccion/serializers.py

from rest_framework import serializers

from apps.login.serializers import UserSerializer

from .models import Producto, Maquina, Turno, RegistroR145

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
        fields = ['id', 'code', 'shift', 'start_time', 'end_time']

class RegistroR145Serializer(serializers.ModelSerializer):
    producto = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Producto.objects.all()
    )
    maquina = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Maquina.objects.all()
    )
    turno = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Turno.objects.all()
    )

    operario = UserSerializer(read_only=True)
    revisador = UserSerializer(read_only=True)
    auxiliar = UserSerializer(read_only=True)

    hora_inicio = serializers.TimeField(format="%H:%M", input_formats=["%H:%M"])
    hora_fin = serializers.TimeField(format="%H:%M", input_formats=["%H:%M"])
    extension_hora = serializers.TimeField(format="%H:%M", input_formats=["%H:%M"])

    class Meta:
        model = RegistroR145
        fields = '__all__'
        read_only_fields = [
            'operario', 'revisador', 'auxiliar',
            'fecha_operario', 'fecha_revisador',
            'fecha_auxiliar', 'fase', 'estado'
        ]