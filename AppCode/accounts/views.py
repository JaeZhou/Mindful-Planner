from django.shortcuts import render

# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class ScheduleView(generic.CreateView):
    success_url = reverse_lazy('schedule')
    template_name = 'schedule.html'