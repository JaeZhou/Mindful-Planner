# to-do-list/urls.py
from django.urls import path
from .views import ToDoList, TaskCreate, TaskEdit, TaskDelete, SubtaskList, SubtaskCreate, SubtaskEdit, SubtaskDelete
from django.views.generic.base import TemplateView


urlpatterns = [
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-edit/<int:pk>/', TaskEdit.as_view(), name='task-edit'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('subtask-create/', SubtaskCreate.as_view(), name='subtask-create'),
    path('subtask-edit/<int:pk>/', SubtaskEdit.as_view(), name='subtask-edit'),
    path('subtask-delete/<int:pk>/', SubtaskDelete.as_view(), name='subtask-delete'),
]