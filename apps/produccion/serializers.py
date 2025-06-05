# produccion/serializers.py

from rest_framework import serializers

from apps.login.serializers import UserSerializer
from core import settings

from .models import Producto, Maquina, Turno, RegistroR145
from .models import Turno, TurnoTrabajo, AsignacionTurno

from django.contrib.auth import get_user_model



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

class TurnoTrabajoSerializer(serializers.ModelSerializer):
    # Para escritura (input): acepta solo el `code` del turno
    turno = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Turno.objects.all(),
        write_only=True
    )

    # Para lectura (output): retorna todo el turno anidado
    turno_obj = TurnoSerializer(source='turno', read_only=True)

    class Meta:
        model = TurnoTrabajo
        fields = ['id', 'fecha', 'turno', 'turno_obj', 'code']

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # renombrar 'turno_obj' a 'turno' en la salida
        rep['turno'] = rep.pop('turno_obj', None)
        return rep




User = get_user_model()

class AsignacionTurnoSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='usuario.role', read_only=True)

    turno_trabajo = serializers.SlugRelatedField(
        slug_field='code',
        queryset=TurnoTrabajo.objects.all()
    )

    usuario = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = AsignacionTurno
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Turno de trabajo anidado
        rep['turno_trabajo'] = TurnoTrabajoSerializer(instance.turno_trabajo).data

        # Usuario anidado con username y role
        rep['usuario'] = UserSerializer(instance.usuario).data

        return rep




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