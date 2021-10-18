from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.all_tasks, name='ds'),
    path('task-delete/<id>/', views.delete_task, name='task-delete'),
    path('task-edit/<id>/', views.edit_task, name='task-edit'),
    path('event-delete/<id>/', views.delete_event, name='event-delete')
]
