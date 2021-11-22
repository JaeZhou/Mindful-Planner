# to-do-list/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task, Subtask

#List view for the to do list
class ToDoList(ListView):
    model = Task
    template_name = 'tables.html'
    
    def get_queryset(self):
        tasks = self.model.objects.filter(user=self.request.user)
        return tasks

    def get_context_data(self, **kwargs):
        context = super(ToDoList, self).get_context_data(**kwargs)
        context['tasks'] = self.model.objects.filter(user=self.request.user)
        return context

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

class SubtaskList(ListView):
    model = Subtask
    context_object_name = 'subtasks'

#Task creating view in task_form.html
class SubtaskCreate(CreateView):
    model = Subtask
    template_name = 'subtask_form.html'
    #No user field needed
    fields = ['name', 'complete']
    success_url = reverse_lazy('tables')
    #Validates that user form is valid
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SubtaskCreate, self).form_valid(form)

#Task editing view in task_form.html
class SubtaskEdit(UpdateView):
    model = Subtask
    template_name = 'subtask_form.html'
    #No user field needed
    fields = ['name', 'complete']
    success_url = reverse_lazy('tables')

#Task deleting view in task_form.html
class SubtaskDelete(DeleteView):
    model = Subtask
    template_name = 'subtask_delete.html'
    context_object_name = 'subtask'
    success_url = reverse_lazy('tables')