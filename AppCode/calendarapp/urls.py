from django.urls import path
from .views import Calendar, EventCreate, EventEdit, EventDelete
from django.views.generic.base import TemplateView

urlpatterns = [
    path('event-create/', EventCreate.as_view(), name='event-create'),
    path('event-edit/<int:pk>/', EventEdit.as_view(), name='event-edit'),
    path('event-delete/<int:pk>/', EventDelete.as_view(), name='event-delete'),
]