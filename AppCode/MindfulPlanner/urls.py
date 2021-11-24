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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from todolist.views import ToDoList
from MindfulPlanner import views
import notifications.urls
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('customers/', include("customers.urls")),
    path('todolist/', include('todolist.urls')),
    # url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # The home page
    path('dashboard/', views.index, name='home'),

    path('', TemplateView.as_view(template_name='mainpage.html'), name='hp'),
    path('tables/', ToDoList.as_view(template_name='tables.html'), name='tables'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]