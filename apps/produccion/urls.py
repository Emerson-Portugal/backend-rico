from django.urls import path
from .views import ProductoViewSet, MaquinaViewSet, TurnoViewSet, RegistroR145ViewSet, TurnoTrabajoViewSet, AsignacionTurnoViewSet

# Producto
producto_detail = ProductoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

producto_list_create = ProductoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# Maquina
maquina_detail = MaquinaViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

maquina_list_create = MaquinaViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# Turno
turno_detail = TurnoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

turno_list_create = TurnoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# RegistroR145
registro_detail = RegistroR145ViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

registro_list_create = RegistroR145ViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# TurnoTrabajo
turno_trabajo_list_create = TurnoTrabajoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
turno_trabajo_detail = TurnoTrabajoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

# AsignacionTurno
asignacion_list_create = AsignacionTurnoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
asignacion_detail = AsignacionTurnoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
asignacion_por_usuario = AsignacionTurnoViewSet.as_view({
    'get': 'por_usuario'
})

urlpatterns = [
    # Productos
    path('productos/', producto_list_create, name='producto-list-create'),
    path('productos/<str:code>/', producto_detail, name='producto-detail'),

    # Maquinas
    path('maquinas/', maquina_list_create, name='maquina-list-create'),
    path('maquinas/<str:code>/', maquina_detail, name='maquina-detail'),

    # Turnos
    path('turnos/', turno_list_create, name='turno-list-create'),
    path('turnos/<str:code>/', turno_detail, name='turno-detail'),

        # Registros de Producción R145
    path('registrosR145/', registro_list_create, name='registror145-list-create'),
    path('registrosR145/<str:code>/', registro_detail, name='registror145-detail'),

    path('turnos-trabajo/', turno_trabajo_list_create, name='turno-trabajo-list-create'),
    path('turnos-trabajo/<str:code>/', turno_trabajo_detail, name='turno-trabajo-detail'),

    path('asignaciones-turno/', asignacion_list_create, name='asignacion-turno-list-create'),
    path('asignaciones-turno/<str:code>/', asignacion_detail, name='asignacion-turno-detail'),
    path('asignaciones-turno/por-usuario/<str:username>/', asignacion_por_usuario, name='asignacion-turno-por-usuario'),
]

