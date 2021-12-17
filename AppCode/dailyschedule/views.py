
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from todolist.models import Task, Subtask
from calendarapp.models import Event
from django.contrib import messages
from django.http import HttpResponseRedirect
import datetime
from .forms import SubtaskForm, TaskForm, EventForm


@login_required
def all_tasks(request):
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
    form = EventForm(instance=event)
    context = {'event':event, 'form':form}

    if event.user == request.user:
        event.title = request.POST.get('title')
        day = request.POST.get('day')
        print(day)
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

# def delete_event(request, id):
#     event = get_object_or_404(Event, pk=id)
#     context = {'event': event}

#     if event.user == request.user:
#         event.delete()
#         messages.add_message(request, messages.SUCCESS, "Event Deleted.")

#         return HttpResponseRedirect(reverse('ds'))

#     return render(request, 'schedule.html', context)

#Task deleting view in task_form.html
class EventDelete(DeleteView):
    model = Event
    template_name = 'event_delete.html'
    # context_object_name = 'task'
    success_url = reverse_lazy('ds')

def subtask_view(request, id):
    t = Task.objects.get(id=id)
    subtasks = t.subtask_set.all()
    return render(request, 'subtasks.html', {'subtasks': subtasks})

#Task creating view in task_form.html
class SubtaskCreate(CreateView):
    template_name = 'subtask_form.html'
    form_class = SubtaskForm
    success_url = reverse_lazy('todolist')

    def get_initial(self):
        initial=super(SubtaskCreate, self).get_initial()
        initial['task'] = Task.objects.get(pk=self.kwargs['pk'])
        return initial

#Task editing view in task_form.html
class SubtaskEdit(UpdateView):
    model = Subtask
    form_class = SubtaskForm    
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('todolist')

    def get_context_data(self, **kwargs):
        st = Subtask.objects.get(pk = self.kwargs['pk'])
        st.complete = not st.complete
        st.save()
        context = super(SubtaskEdit, self).get_context_data(**kwargs)
        return context    

#Task deleting view in task_form.html
class SubtaskDelete(DetailView):
    model = Subtask
    template_name = 'subtask_delete.html'
    context_object_name = 'subtask'
    success_url = reverse_lazy('todolist')

    def get_context_data(self, **kwargs):
        st = Subtask.objects.get(pk = self.kwargs['pk'])
        st.remove()
        context = super(SubtaskEdit, self).get_context_data(**kwargs)
        return context    

class SubtaskRerenderView(ListView):
    model = Subtask
    template_name = 'subtasks.html'
    success_url = reverse_lazy('todolist')

    def get_context_data(self, **kwargs):
        context = super(SubtaskRerenderView, self).get_context_data(**kwargs)
        t = Task.objects.get(id=self.kwargs['pk'])
        subtasks = t.subtask_set.all()
        context['subtasks'] = subtasks
        return context

class DailyScheduleListRerender(ListView):
    model = Task
    events = Event
    template_name = 'rr_tasks.html'
    
    def get_queryset(self):
        tasks = self.model.objects.filter(user=self.request.user)
        events = self.events.objects.filter(user=self.request.user)
        return [tasks, events]

    def get_context_data(self, **kwargs):
        context = super(DailyScheduleListRerender, self).get_context_data(**kwargs)
        context['tasks'] = self.model.objects.filter(user=self.request.user)
        context['events'] = self.events.objects.filter(user=self.request.user)
        return context  