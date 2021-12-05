from django import forms
from .models import Task, Subtask
from django.core.exceptions import ValidationError

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

    # def clean(self):
    #     cleaned_data = super(TaskForm, self).clean()

    #     name = cleaned_data.get('name')
    #     due_date = cleaned_data.get('due_date')
    #     due_time = cleaned_data.get('due_time')

    #     if not name:
    #         print("WTF")
    #         self.add_error(name, "Name field cannot be empty.")

    #     return self.cleaned_data

class SubtaskForm(forms.ModelForm):
  
    # create meta class
    class Meta:
        # specify model to be used
        model = Subtask
  
        # specify fields to be used
        fields = ["task", "name", "complete"]
        widgets = {"task": forms.HiddenInput(), "complete": forms.HiddenInput(),}