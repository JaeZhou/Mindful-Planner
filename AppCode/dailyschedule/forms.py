from django import forms
from todolist.models import Subtask
from calendarapp.models import Event
from todolist.models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = "__all__"

class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = ['title', 'day', 'startTime', 'endTime', 'description']

class SubtaskForm(forms.ModelForm):
  
    # create meta class
    class Meta:
        # specify model to be used
        model = Subtask
  
        # specify fields to be used
        fields = ["task", "name", "complete"]
        widgets = {"task": forms.HiddenInput(), "complete": forms.HiddenInput(),}