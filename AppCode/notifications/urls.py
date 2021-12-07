# to-do-list/urls.py
from django.urls import path, include
from django.views.generic.base import TemplateView
import notifications.urls
from django.conf.urls import url
from . import views

app_name = 'notifications'

urlpatterns = [
    #url(r'^inbox/notifications/', include('notifications.urls', namespace='notifications')),

    path('export_csv/<choice>/', views.export_respone, name='export_csv')
]