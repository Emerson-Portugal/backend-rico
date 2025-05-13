
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', include('apps.login.urls')),
    path('api/produccion', include('apps.produccion.urls')),
]
