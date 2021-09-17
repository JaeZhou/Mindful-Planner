# to-do-list/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task

class ToDoList(ListView):
    model = Task
    template_name = 'tables.html'
    context_object_name = 'tasks'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['tasks'] = context['tasks'].filter(user=self.request.user)
    #     return context

class TaskCreate(CreateView):
    model = Task
    template_name = 'task_form.html'
    fields = ['name', 'complete', 'due_date', 'due_time']
    success_url = reverse_lazy('tables')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskEdit(UpdateView):
    model = Task
    template_name = 'task_form.html'
    fields = '__all__'
    success_url = reverse_lazy('tables')

class TaskDelete(DeleteView):
    model = Task
    template_name = 'task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tables')