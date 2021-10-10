
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse
from todolist.models import Task
from calendarapp.models import Event
from django.contrib import messages
from django.http import HttpResponseRedirect
import datetime


# class SearchTasks(ListView):
#     model = Task
#     template_name = 'schedule.html'
#     context_object_name = 'tasks'


def all_tasks(request):
    #TODO fix this timezone stuff
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
        print('delete')
        messages.add_message(request, messages.SUCCESS, "Task Deleted.")

        return HttpResponseRedirect(reverse('ds'))

    return render(request, 'schedule.html', context)
