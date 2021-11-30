from django import forms
from .models import Task, Subtask

class SubtaskForm(forms.ModelForm):
  
    # create meta class
    class Meta:
        # specify model to be used
        model = Subtask
  
        # specify fields to be used
        fields = ["task", "name"]
        widgets = {"task": forms.HiddenInput()}