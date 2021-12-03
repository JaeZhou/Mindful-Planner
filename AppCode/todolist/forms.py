from django import forms
from .models import Task, Subtask

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

class SubtaskForm(forms.ModelForm):
  
    # create meta class
    class Meta:
        # specify model to be used
        model = Subtask
  
        # specify fields to be used
        fields = ["task", "name", "complete"]
        widgets = {"task": forms.HiddenInput(), "complete": forms.HiddenInput(),}