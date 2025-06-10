from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.forms import ValidationError
from rest_framework import viewsets, permissions, status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from apps.produccion.models import Producto, Maquina, Turno, RegistroR145
from apps.produccion.models.turno import AsignacionTurno, TurnoTrabajo
from .serializers import AsignacionTurnoSerializer, ProductoSerializer, MaquinaSerializer, TurnoSerializer, RegistroR145Serializer, TurnoTrabajoSerializer, User
from .pagination import CustomPagination
from apps.produccion.utils.turno_utils import obtener_usuarios_en_turno_actual, obtener_asignacion_usuario_en_turno_actual
from apps.produccion.utils.notificaciones import notificar_a_usuarios
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError



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
    lookup_field = 'code'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        return Response({"data": data})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)

        data = self.get_serializer(queryset, many=True).data
        return Response({"data": data})



class AsignacionTurnoViewSet(viewsets.ModelViewSet):
    queryset = AsignacionTurno.objects.all()
    serializer_class = AsignacionTurnoSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = 'code'

    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        usuario = serializer.validated_data['usuario']
        turno_trabajo = serializer.validated_data['turno_trabajo']

        if AsignacionTurno.objects.filter(
            turno_trabajo=turno_trabajo,
            usuario=usuario
        ).exists():
            raise ValidationError("Este usuario ya está asignado a ese turno de trabajo.")
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        return Response({"data": data})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)

        data = self.get_serializer(queryset, many=True).data
        return Response({"data": data})

    @action(detail=False, url_path='por-usuario/(?P<username>[^/.]+)', methods=['get'])
    def por_usuario(self, request, username=None):
        usuario = get_object_or_404(User, username=username)
        asignaciones = AsignacionTurno.objects.filter(usuario=usuario)
        page = self.paginate_queryset(asignaciones)

        if page is not None:
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)

        data = self.get_serializer(asignaciones, many=True).data
        return Response({"data": data})




		
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
            # Solo ve productos oficialmente en fase REVISADOR
            return RegistroR145.objects.filter(fase='REVISADOR')

        elif user.role == 'AUXILIAR':
            # AUXILIAR ve productos en fase OPERARIO o REVISADOR, o donde participó
            return RegistroR145.objects.filter(
                Q(fase__in=['OPERARIO', 'REVISADOR'])
            )

        return RegistroR145.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page is not None else queryset, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response({"data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data})

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != 'OPERADOR':
            raise ValidationError("Solo los operarios pueden registrar productos.")

        # Validar que el usuario está en un turno activo ahora
        asignacion_turno = obtener_asignacion_usuario_en_turno_actual(user)
        if not asignacion_turno:
            raise ValidationError("No estás en tu turno asignado en este momento. No puedes registrar productos ahora.")

        # Verificar que el operario no tenga productos sin finalizar
        productos_pendientes = RegistroR145.objects.filter(
            operario=user
        ).exclude(fase='FINALIZADO')

        for prod in productos_pendientes:
            if not (prod.recor and prod.peso and prod.dm and prod.vacio):
                raise ValidationError({
                    'detalle': "Debes esperar a que el producto anterior sea completamente revisado y finalizado."
                })

        serializer.save(
            operario=user,
            turno=asignacion_turno,  # importante: guarda la asignación de turno usada
            fase='OPERARIO',
            estado='EN_PROCESO',
            fecha_operario=timezone.now()
        )

        usuarios_turno = obtener_usuarios_en_turno_actual()
        if usuarios_turno.get('AUXILIAR'):
            notificar_a_usuarios(usuarios_turno['AUXILIAR'], "🟢 Se ha creado un nuevo producto. Puedes empezar a llenar D.M. y Vacío.")
        if usuarios_turno.get('SUPERVISOR'):
            notificar_a_usuarios(usuarios_turno['SUPERVISOR'], "🟢 Un operario ha registrado un nuevo producto.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"data": serializer.data})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        data = request.data
        usuarios_turno = obtener_usuarios_en_turno_actual()

        # OPERADOR finaliza la fase OPERARIO → pasa a REVISADOR
        if user.role == 'OPERADOR' and instance.fase == 'OPERARIO':
            instance.hora_fin = data.get('hora_fin')
            instance.unidades_kilos = data.get('unidades_kilos')
            instance.golpe = data.get('golpe')
            instance.fecha_operario_fin = timezone.now()
            instance.fase = 'REVISADOR'

            if usuarios_turno:
                if usuarios_turno.get('REVISADOR'):
                    notificar_a_usuarios(usuarios_turno['REVISADOR'], "🔵 Producto listo para revisión.")
                if usuarios_turno.get('AUXILIAR'):
                    notificar_a_usuarios(usuarios_turno['AUXILIAR'], "🔵 Producto en revisión. Finaliza tu parte si no lo hiciste.")
                if usuarios_turno.get('SUPERVISOR'):
                    notificar_a_usuarios(usuarios_turno['SUPERVISOR'], "🔵 Un producto ha sido terminado por el operario.")

        # REVISADOR revisa el producto en fase REVISADOR
        elif user.role == 'REVISADOR':
            if instance.fase != 'REVISADOR':
                return Response({"error": "No puedes revisar este producto hasta que la fase REVISADOR inicie."}, status=403)

            instance.recor = data.get('recor')
            instance.peso = data.get('peso')
            instance.revisador = user
            instance.fecha_revisador = timezone.now()


            if usuarios_turno:
                if usuarios_turno.get('OPERADOR'):
                    notificar_a_usuarios(usuarios_turno['OPERADOR'], "🔵 Producto ha sido revisado por el Revisador")
                if usuarios_turno.get('AUXILIAR'):
                    notificar_a_usuarios(usuarios_turno['AUXILIAR'], "🔵 Producto ha sido revisado por el Revisador")
                if usuarios_turno.get('SUPERVISOR'):
                    notificar_a_usuarios(usuarios_turno['SUPERVISOR'], "🔵 Producto ha sido revisado por el Revisador")


        # AUXILIAR puede completar D.M. y Vacío en fase OPERARIO o REVISADOR
        elif user.role == 'AUXILIAR':
            if instance.fase not in ['OPERARIO', 'REVISADOR']:
                return Response({"error": "No puedes editar este producto en esta fase."}, status=403)

            instance.dm = data.get('dm', instance.dm)
            instance.vacio = data.get('vacio', instance.vacio)
            instance.auxiliar = user

            if not instance.fecha_auxiliar:
                instance.fecha_auxiliar = timezone.now()

            if usuarios_turno:
                if usuarios_turno.get('OPERADOR'):
                    notificar_a_usuarios(usuarios_turno['OPERADOR'], "🔵 Producto ha sido revisado por el Auxiliar")
                if usuarios_turno.get('REVISADOR'):
                    notificar_a_usuarios(usuarios_turno['REVISADOR'], "🔵 Producto ha sido revisado por el Auxiliar")
                if usuarios_turno.get('SUPERVISOR'):
                    notificar_a_usuarios(usuarios_turno['SUPERVISOR'], "🔵 Producto ha sido revisado por el Auxiliar")

        else:
            return Response({"error": "No puedes modificar este producto en esta fase."}, status=403)

        # Finalización automática cuando todos han completado
        if all([instance.recor, instance.peso, instance.dm, instance.vacio]):
            instance.fase = 'FINALIZADO'
            instance.estado = 'FINALIZADO'

            if usuarios_turno:
                if usuarios_turno.get('OPERADOR'):
                    notificar_a_usuarios(usuarios_turno['OPERADOR'], "✅ Producto finalizado. Ya puedes registrar uno nuevo.")
                if usuarios_turno.get('AUXILIAR'):
                    notificar_a_usuarios(usuarios_turno['AUXILIAR'], "🔵 Producto finalizado.")
                if usuarios_turno.get('REVISADOR'):
                    notificar_a_usuarios(usuarios_turno['REVISADOR'], "🔵 Producto finalizado.")

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data})







