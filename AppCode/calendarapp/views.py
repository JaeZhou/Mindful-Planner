#calendarapp/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Event

#List view for calendar
class Calendar(ListView):
    model = Event
    template_name = 'calendar.html'
    context_object_name = 'events'

#Event creating view in event_form.html
class EventCreate(CreateView):
    model = Event
    template_name = "event-form.html"
    fields = ['title', 'day', 'startTime', 'endTime', 'description']
    success_url = reverse_lazy('calendar')

    #Validates that user form is valid
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreate, self).form_valid(form)
    
#Event editing view in task_edit
class EventEdit(UpdateView):
    model = Event
    template_name = 'event-form.html'
    fields = ['title', 'day', 'startTime', 'endTime', 'description', 'complete']
    success_url = reverse_lazy('calendar')

#Event delete view 
class EventDelete(DeleteView):
    model = Event
    template_name = 'event-delete.html'
    context_object_name = 'event'
    success_url = reverse_lazy('calendar')