# -*- encoding: utf-8 -*-


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib.auth.models import User
from todolist.models import Task
from calendarapp.models import Event



# Loads Dashboard Page
@login_required
def index(request):
    
    context = {}
    context['segment'] = 'index'

    # Generate the task list and event list
    task_list = Task.objects.filter(user=request.user)
    event_list = Event.objects.filter(user=request.user)
    context['tasks'] = task_list
    context['events'] = event_list

    graph = [50, 40, 300, 220, 500, 250, 400, 230, 500]
    context['data_set'] = graph
    

    html_template = loader.get_template( 'index.html')
    return HttpResponse(html_template.render(context, request))

# Loads Landing Page
@login_required
def mainpage(request):
    context = {}
    context['segment'] = 'index'
    html_template = loader.get_template( 'mainpage.html' )
    return HttpResponse(html_template.render(context, request))

@login_required
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))