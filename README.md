# Django Rest Framework - API RESTful
pip install django djangorestframework django-cors-headers django-filter

# Crear requerimiento
pip freeze > requirements.txt

## Crear proyecto Inicial
django-admin startproject core .

## Crear app inicial
django-admin startapp "nombre_app"

## Para ejecutar el servidor
python manage.py runserver

## Crear migraciones
python manage.py makemigrations
python manage.py migrate


## Ejecutar Django limpiando cache
python manage.py clear_cache
python manage.py runserver --noreload
python manage.py runserver --noreload --insecure

## Ejecutar Django 
python manage.py runserver