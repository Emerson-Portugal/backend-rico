from django.utils import timezone
from django.forms import ValidationError
from rest_framework import viewsets, permissions, status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from apps.produccion.models import Producto, Maquina, Turno, RegistroR145
from apps.produccion.models.turno import AsignacionTurno, TurnoTrabajo
from .serializers import AsignacionTurnoSerializer, ProductoSerializer, MaquinaSerializer, TurnoSerializer, RegistroR145Serializer, TurnoTrabajoSerializer
from .pagination import CustomPagination
from apps.produccion.utils.turno_utils import obtener_usuarios_en_turno_actual, obtener_turno_actual
from apps.produccion.utils.notificaciones import notificar_a_usuarios
from rest_framework.response import Response


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'code'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        return Response({"data": data})

class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer
    lookup_field = 'code'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        return Response({"data": data})

class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    lookup_field = 'code'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        return Response({"data": data})


class TurnoTrabajoViewSet(viewsets.ModelViewSet):
    queryset = TurnoTrabajo.objects.all()
    serializer_class = TurnoTrabajoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

class AsignacionTurnoViewSet(viewsets.ModelViewSet):
    queryset = AsignacionTurno.objects.all()
    serializer_class = AsignacionTurnoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        usuario = serializer.validated_data['usuario']
        turno_trabajo = serializer.validated_data['turno_trabajo']

        # Validar que el usuario no esté asignado dos veces el mismo día
        if AsignacionTurno.objects.filter(
            turno_trabajo__fecha=turno_trabajo.fecha,
            usuario=usuario
        ).exists():
            raise ValidationError("Este usuario ya está asignado a un turno ese día.")

        serializer.save()







class RegistroR145ViewSet(viewsets.ModelViewSet):
    queryset = RegistroR145.objects.all()
    serializer_class = RegistroR145Serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    lookup_field = 'code'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'OPERADOR':
            return RegistroR145.objects.filter(operario=user)
        elif user.role == 'REVISADOR':
            return RegistroR145.objects.filter(Q(fase='OPERARIO') | Q(revisador=user))
        elif user.role == 'AUXILIAR':
            return RegistroR145.objects.filter(Q(fase='REVISADOR') | Q(auxiliar=user))
        else:
            return RegistroR145.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Pasa solo la lista al paginated_response
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response({"data": data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return Response({"data": data})

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != 'OPERADOR':
            raise ValidationError("Solo los operarios pueden registrar productos.")
        if RegistroR145.objects.filter(operario=user).exclude(fase='FINALIZADO').exists():
            raise ValidationError("Debes finalizar el producto anterior antes de registrar uno nuevo.")

        serializer.save(
            operario=user,
            fase='OPERARIO',
            fecha_operario=timezone.now()
        )

        # 🔔 Notificar a revisadores del turno actual
        # Dentro de perform_create en RegistroR145ViewSet
        usuarios_turno = obtener_usuarios_en_turno_actual()
        print("📌 Usuarios en turno actual:", usuarios_turno)
        if usuarios_turno and usuarios_turno['REVISADOR']:
            notificar_a_usuarios(usuarios_turno['REVISADOR'], "Un nuevo producto ha sido registrado para revisión.")



    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        return Response({"data": data})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        # Dentro de perform_create en RegistroR145ViewSet
        usuarios_turno = obtener_usuarios_en_turno_actual()
        print("📌 Usuarios en turno actual:", usuarios_turno)
        if usuarios_turno and usuarios_turno['REVISADOR']:
            notificar_a_usuarios(usuarios_turno['REVISADOR'], "Un nuevo producto ha sido registrado para revisión.")


        # Fase de revisión
        if user.role == 'REVISADOR' and instance.fase == 'OPERARIO':
            instance.fase = 'REVISADOR'
            instance.estado = 'EN_PROCESO'
            instance.revisador = user
            instance.fecha_revisador = timezone.now()

            if usuarios_turno and usuarios_turno['AUXILIAR']:
                notificar_a_usuarios(usuarios_turno['AUXILIAR'], "Un producto ha sido revisado y está listo para finalizar.")
        
        # Fase de finalización
        elif user.role == 'AUXILIAR' and instance.fase == 'REVISADOR':
            instance.fase = 'FINALIZADO'
            instance.estado = 'FINALIZADO'
            instance.auxiliar = user
            instance.fecha_auxiliar = timezone.now()

            if usuarios_turno and usuarios_turno['OPERADOR']:
                notificar_a_usuarios(usuarios_turno['OPERADOR'], "Un producto ha sido finalizado. Puedes registrar uno nuevo.")
        
        else:
            return Response({"error": "No puedes modificar este producto en esta fase."}, status=403)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data})
