from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('celery_status/', views.celery_status, name='celery_status'),
    path('celery_status/<str:task_id>/', views.celery_status, name='celery_status_task'),
    path('write_randoms/', views.write_randoms, name='write_randoms'),
    path('read_randoms/', views.read_randoms, name='read_randoms'),
    path('clear_randoms/', views.clear_randoms, name='clear_randoms'),
]