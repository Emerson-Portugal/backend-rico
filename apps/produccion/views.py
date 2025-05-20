from django.utils import timezone

from django.forms import ValidationError
from rest_framework import viewsets, permissions, status
from django.db.models import Q


from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from apps.produccion.models import Producto, Maquina, Turno, RegistroR145
from .serializers import ProductoSerializer, MaquinaSerializer, TurnoSerializer, RegistroR145Serializer
from .pagination import CustomPagination


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        return Response({"data": data})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        # Fase de revisión
        if user.role == 'REVISADOR' and instance.fase == 'OPERARIO':
            instance.fase = 'REVISADOR'
            instance.estado = 'EN_PROCESO'
            instance.revisador = user
            instance.fecha_revisador = timezone.now()
        # Fase de auxiliar
        elif user.role == 'AUXILIAR' and instance.fase == 'REVISADOR':
            instance.fase = 'FINALIZADO'
            instance.estado = 'FINALIZADO'
            instance.auxiliar = user
            instance.fecha_auxiliar = timezone.now()
        else:
            return Response({"error": "No puedes modificar este producto en esta fase."}, status=403)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response({"data": data})