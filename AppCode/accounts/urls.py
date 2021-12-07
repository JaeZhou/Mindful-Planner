# accounts/urls.py
from django.contrib.auth import logout
from django.urls import path

from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('logout/', views.logout_user, name='logout'),
]