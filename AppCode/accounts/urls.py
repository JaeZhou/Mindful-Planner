# accounts/urls.py
from AppCode.MindfulPlanner.settings import LOGIN_REDIRECT_URL
from django.urls import path

from .views import SignUpView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', )
]