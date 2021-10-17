# to-do-list/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task

#List view for the to do list
class ToDoList(ListView):
    model = Task
    template_name = 'tables.html'
    context_object_name = 'tasks'

#Task creating view in task_form.html
class TaskCreate(CreateView):
    model = Task
    template_name = 'task_form.html'
    #No user field needed
    fields = ['name', 'complete', 'due_date', 'due_time']
    success_url = reverse_lazy('tables')
    #Validates that user form is valid
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

#Task editing view in task_form.html
class TaskEdit(UpdateView):
    model = Task
    template_name = 'task_form.html'
    #No user field needed
    fields = ['name', 'complete', 'due_date', 'due_time']
    success_url = reverse_lazy('tables')

#Task deleting view in task_form.html
class TaskDelete(DeleteView):
    model = Task
    template_name = 'task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tables')

def orderTasks(request):
    #get all tasks
    allTasks = Task.objects.all()
    #sort by day and time
    sortedTasks = Task.objects.order_by('due_date').order_by('due_time')

    context = {'allsortedTasks': sortedTasks}

    return render(request, 'tables', context)