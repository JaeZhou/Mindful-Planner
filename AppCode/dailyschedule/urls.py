from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.all_tasks, name='ds'),
    path('task-delete/<id>/', views.delete_task, name='task-delete')
]
