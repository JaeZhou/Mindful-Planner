from django.shortcuts import render

# accounts/views.py
from accounts.forms import RegistrationForm 
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'