# to-do-list/urls.py
from django.urls import path
from .views import ToDoList, ToDoListRerender, TaskCreate, TaskEdit, TaskDelete, SubtaskView, SubtaskRerenderView, SubtaskCreate, SubtaskEdit, SubtaskDelete
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from . import views



urlpatterns = [
    path('', login_required(ToDoList.as_view(template_name='todolist.html')), name='todolist'),
    path('rerender/', login_required(ToDoListRerender.as_view(template_name='rerender_tasks.html')), name='todolist-rerender'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-edit/<int:pk>/', TaskEdit.as_view(), name='task-edit'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('subtasks/<int:pk>', SubtaskView.as_view(), name='subtasks'),
    path('subtasks-rerender/<int:pk>', SubtaskRerenderView.as_view(), name='subtasks-rerender'),
    path('subtask-create/<int:pk>/', SubtaskCreate.as_view(), name='subtask-create'),
    path('subtask-edit/<int:pk>/', SubtaskEdit.as_view(), name='subtask-edit'),
    path('subtask-delete/<int:pk>/', SubtaskDelete.as_view(), name='subtask-delete'),
]