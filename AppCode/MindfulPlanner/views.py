# -*- encoding: utf-8 -*-


from os import name
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
import pandas as pd
from django.contrib.auth.models import User
from todolist.models import Task
from calendarapp.models import Event



# Loads Dashboard Page
@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

def index(request):
    df = pd.read_csv('user_schedule_update.xls')
    context = {}
    context['graph'] = 'plot_div'
    x_data = df['Hour'].head(24)
    y_data = df['Make_Schedule_count_byweek']
    # plot_div = go.Scatter(
    #             x =x_data,
    #             y =y_data,
    #             name = "Predicted hours",
    #             marker = dict(color = 'rgb(178, 102, 255)'))

    # fig = go.Layout(title="Predicted Hours this week",
    #                xaxis= dict(title= 'Hour',ticklen= 5,zeroline= False), 
    #                yaxis= dict(title= 'Total Booking Counts',ticklen= 5,zeroline= False))
   
  
    plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.5, marker_color='green')],
                        output_type='div')

    # layout = go.Layout(title = 'Line Plot: Mean House Values by Bedrooms and Year',
    #           xaxis= dict(title= 'Year',ticklen= 5,zeroline= False),
    #           yaxis= dict(title= 'Mean House Values',ticklen= 5,zeroline= False)
    #          )
    # fig = go.Figure(data = plot_div, layout = fig)
    
    return render(request, "index.html", context={'plot_div': plot_div})
    # return render(request, "index.html", context={'plot_div': fig})


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
def mainpage(request):
    context = {}
    context['segment'] = 'index'
    html_template = loader.get_template( 'mainpage.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
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