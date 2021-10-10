
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse
from todolist.models import Task
from calendarapp.models import Event
from django.contrib import messages
from django.http import HttpResponseRedirect
import datetime
from .forms import TaskForm


# class SearchTasks(ListView):
#     model = Task
#     template_name = 'schedule.html'
#     context_object_name = 'tasks'


def all_tasks(request):
    today = datetime.date.today()
    task_list = Task.objects.filter(user=request.user, due_date=today)
    event_list = Event.objects.filter(user=request.user, day=today)
    context = {'tasks':task_list, 'events':event_list}
    return render(request, 'schedule.html', context)

def delete_task(request, id):
    task = get_object_or_404(Task, pk=id)
    context = {'task': task}
    
    
    if task.user == request.user:
        task.delete()
        messages.add_message(request, messages.SUCCESS, "Task Deleted.")

        return HttpResponseRedirect(reverse('ds'))

    return render(request, 'schedule.html', context)

def edit_task(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)
    context = {'task':task, 'form':form}

    if task.user == request.user:
        name = request.POST.get('name')

        task.name = name

        if task.user == request.user:
            task.save()

        messages.add_message(request, messages.SUCCESS, "Task update success")

        return HttpResponseRedirect(reverse("todo", kwargs={'id': task.pk}))

    return render(request, 'schedule.html', context)


def delete_event(request, id):
    event = get_object_or_404(Event, pk=id)
    context = {'event': event}
    
    
    if event.user == request.user:
        event.delete()
        messages.add_message(request, messages.SUCCESS, "Event Deleted.")

        return HttpResponseRedirect(reverse('ds'))

    return render(request, 'schedule.html', context)
