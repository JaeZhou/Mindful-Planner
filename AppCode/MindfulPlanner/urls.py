"""MindfulPlanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.conf.urls.static import static
from todolist.views import ToDoList
from MindfulPlanner import views
import notifications.urls
from calendarapp.views import Calendar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('customers/', include("customers.urls")),
    path('todolist/', include('todolist.urls')),
    path('inbox/', include('notifications.urls')),
    # url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

    path('dailyschedule/', include('dailyschedule.urls')),
  
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
  
    path('calendarapp/', include('calendarapp.urls')),
    
    # path for result of machine learning
    path('result/', views.result, name='result'),
  
    # The home page
    path('dashboard/', views.index, name='home'),

    path('', TemplateView.as_view(template_name='mainpage.html'), name='hp'),
    path('calendar/', login_required(Calendar.as_view(template_name='calendar.html')), name='calendar'),
    path('timer/', login_required(TemplateView.as_view(template_name='timer.html')), name='timer'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)