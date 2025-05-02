
from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    re_path('login', views.login, name='login'),
    re_path('register', views.register, name='register'),
    re_path('profile', views.profile, name='profile'),
]
