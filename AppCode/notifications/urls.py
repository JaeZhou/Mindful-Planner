# to-do-list/urls.py
from django.urls import path, include
from django.views.generic.base import TemplateView
import notifications.urls
from django.conf.urls import url

app_name = 'notifications'

urlpatterns = [
    url(r'^inbox/notifications/', include('notifications.urls', namespace='notifications')),
]