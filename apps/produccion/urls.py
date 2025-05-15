from django.urls import path
from .views import ProductoViewSet, MaquinaViewSet, TurnoViewSet

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

urlpatterns = [
    # Productos
    path('productos/', producto_list_create, name='producto-list-create'),
    path('productos/<str:code>/', producto_detail, name='producto-detail'),

    # Maquinas
    path('maquinas/', maquina_list_create, name='maquina-list-create'),
    path('maquinas/<int:pk>/', maquina_detail, name='maquina-detail'),

    # Turnos
    path('turnos/', turno_list_create, name='turno-list-create'),
    path('turnos/<int:pk>/', turno_detail, name='turno-detail'),
]
