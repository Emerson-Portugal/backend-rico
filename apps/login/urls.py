
from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    re_path('login', views.login, name='login'),
    re_path(r'^users/register', views.register, name='register'),
    re_path('profile', views.profile, name='profile'),

    # Primero las rutas más específicas
    re_path(r'^users/(?P<user_id>\d+)/update/?$', views.update_user, name='update_user'),
    re_path(r'^users/(?P<user_id>\d+)/delete/?$', views.delete_user, name='delete_user'),

    # Luego la ruta por ID (más general)
    re_path(r'^users/(?P<user_id>\d+)/?$', views.get_user_by_id, name='get_user_by_id'),

    # Por último la general sin ID
    re_path(r'^users/?$', views.get_all_users, name='get_all_users'),
]
