from django import forms
from calendarapp.models import Event
from todolist.models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = ['name', 'due_date', 'due_time']

class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = ['title', 'day', 'startTime', 'endTime', 'description']