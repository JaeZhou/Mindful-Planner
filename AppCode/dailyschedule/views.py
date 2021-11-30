
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse
from todolist.models import Task
from calendarapp.models import Event
from django.contrib import messages
from django.http import HttpResponseRedirect
import datetime

from .forms import TaskForm

from accounts.models import User



# class SearchTasks(ListView):
#     model = Task
#     template_name = 'schedule.html'
#     context_object_name = 'tasks'


def all_tasks(request):
    #fix this timezone stuff
    today = datetime.date.today()
    task_list = Task.objects.filter(user=request.user, due_date__year=today.year, due_date__month=today.month, due_date__day=today.day)
    event_list = Event.objects.filter(user=request.user, day__year=today.year, day__month=today.month, day__day=today.day)
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
        task.name = request.POST.get('name')
        #task.complete = request.POST.get('complete')

        due_date = request.POST.get('due_date')
        task.due_date = datetime.datetime.strptime(due_date, "%m/%d/%Y").strftime("%Y-%m-%d")


        task.due_time = request.POST.get('due_time')

        if task.user == request.user:
            task.save()

        messages.add_message(request, messages.SUCCESS, "Task update success")

        return HttpResponseRedirect(reverse("ds"))

    return render(request, 'schedule.html', context)

def edit_event(request, id):
    event = get_object_or_404(Event, pk=id)
    form = TaskForm(instance=event)
    context = {'event':event, 'form':form}

    if event.user == request.user:
        event.title = request.POST.get('title')
        day = request.POST.get('day')
        event.day = datetime.datetime.strptime(day, "%m/%d/%Y").strftime("%Y-%m-%d")

        event.startTime = request.POST.get('start_time')
        event.endTime = request.POST.get('end_time')
        event.description = request.POST.get('description')
        #event.complete = request.POST.get('complete')

        if event.user == request.user:
            event.save()

        messages.add_message(request, messages.SUCCESS, "Event update success")

        return HttpResponseRedirect(reverse("ds"))

    return render(request, 'schedule.html', context)

def delete_event(request, id):
    event = get_object_or_404(Event, pk=id)
    context = {'event': event}

    if event.user == request.user:
        event.delete()
        messages.add_message(request, messages.SUCCESS, "Event Deleted.")

        return HttpResponseRedirect(reverse('ds'))

    return render(request, 'schedule.html', context)
