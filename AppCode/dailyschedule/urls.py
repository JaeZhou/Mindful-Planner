from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.all_tasks, name='ds'),
    path('task-delete/<id>/', views.delete_task, name='task-delete'),
    path('task-edit/<id>/', views.edit_task, name='task-edit'),
    path('event-edit/<id>/', views.edit_event, name='event-edit'),
    path('event-delete/<id>/', views.delete_event, name='event-delete'),
    path('subtasks/<id>', views.subtask_view, name='subtasks'),
    path('subtask-create/<int:pk>/', views.SubtaskCreate.as_view(), name='subtask-create'),
    path('subtask-edit/<int:pk>/', views.SubtaskEdit.as_view(), name='subtask-edit'),
    path('subtask-delete/<int:pk>/', views.SubtaskDelete.as_view(), name='subtask-delete'),
]
