
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse
from django.views.generic import ListView
from todolist.models import Task
from django.db import models
from django.contrib import messages
from django.http import HttpResponseRedirect
import datetime


# class SearchTasks(ListView):
#     model = Task
#     template_name = 'schedule.html'
#     context_object_name = 'tasks'


def all_tasks(request):
    today = datetime.date.today()
    task_list = Task.objects.filter(user=request.user, due_date=today)
    context = {'tasks':task_list}
    return render(request, 'schedule.html', context)

def delete_task(request, id):
    task = get_object_or_404(Task, pk=id)
    context = {'task': task}
    
    
    if task.user == request.user:
        task.delete()
        print('delete')
        messages.add_message(request, messages.SUCCESS, "Task Deleted.")

        return HttpResponseRedirect(reverse('ds'))

    return render(request, 'schedule.html', context)
