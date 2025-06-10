# produccion/serializers.py

from rest_framework import serializers

from apps.login.serializers import UserSerializer
from core import settings

from .models import Producto, Maquina, Turno, RegistroR145
from .models import Turno, TurnoTrabajo, AsignacionTurno

from django.contrib.auth import get_user_model

User = get_user_model()


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'code', 'name', 'type']

class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = ['id', 'code', 'name']

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ['id', 'code', 'shift', 'start_time', 'end_time']



class TurnoTrabajoSerializer(serializers.ModelSerializer):
    # Escritura: acepta solo el código del turno
    turno = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Turno.objects.all(),
        write_only=True
    )

    # Lectura: retorna todo el objeto turno anidado
    turno_obj = TurnoSerializer(source='turno', read_only=True)

    class Meta:
        model = TurnoTrabajo
        fields = ['id', 'fecha_inicio', 'fecha_fin', 'turno', 'turno_obj', 'code']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Renombrar la salida de 'turno_obj' como 'turno'
        rep['turno'] = rep.pop('turno_obj', None)
        return rep

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            diferencia = (fecha_fin - fecha_inicio).days

            if diferencia < 1:
                raise serializers.ValidationError({
                    'fecha_fin': "La fecha de fin debe ser al menos 1 día después de la fecha de inicio."
                })
            if diferencia > 7:
                raise serializers.ValidationError({
                    'fecha_fin': "La fecha de fin no puede ser más de 7 días después de la fecha de inicio."
                })

        return data






class AsignacionTurnoSerializer(serializers.ModelSerializer):

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
    # Escritura: solo se envía el código
    producto = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Producto.objects.all(),
        write_only=True
    )

    # Lectura: se muestra todo el objeto producto
    producto_obj = ProductoSerializer(source='producto', read_only=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Renombrar la salida de 'turno_obj' como 'turno'
        rep['producto'] = rep.pop('producto_obj', None)
        return rep



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