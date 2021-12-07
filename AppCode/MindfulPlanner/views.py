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

# Libraries supports for Machine Learning part
from statsmodels.tsa.arima.model import ARIMA
from math import sqrt
from statsmodels.compat import lzip
import numpy as np
import statsmodels.api as sm
import pandas as pd

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

def result(request):
    # load dataset
    date_rng = pd.date_range(start='5/01/2021', end='10/30/2021', freq='H')
    df = pd.DataFrame(date_rng, columns=['Time'])
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
    df['Hour'] = df['Time'].dt.hour

    df1 = df[df['Hour'] < 8]
    df2 = df[(df['Hour'] >= 8) & (df['Hour'] < 12)]
    df3 = df[(df['Hour'] >= 12) & (df['Hour'] < 15)]
    df4 = df[(df['Hour'] >= 15) & (df['Hour'] < 18)]
    df5 = df[(df['Hour'] >= 18) & (df['Hour'] < 24)]
    #################################Make Schedule######################################################
    df1['Make_Schedule'] = np.random.choice([1, 0], size=(len(df1)), p=[.10, .90])
    df2['Make_Schedule'] = np.random.choice([1, 0], size=(len(df2)), p=[.25, .75])
    df3['Make_Schedule'] = np.random.choice([1, 0], size=(len(df3)), p=[.35, .65])
    df4['Make_Schedule'] = np.random.choice([1, 0], size=(len(df4)), p=[.60, .40])
    df5['Make_Schedule'] = np.random.choice([1, 0], size=(len(df5)), p=[.20, .80])

    df_schedule = pd.concat([df1, df2, df3, df4, df5])
    df_schedule = df_schedule.sort_values(by="Time")

    ##################################Extrct Day/month/year#############################################
    df_schedule['Day'] = pd.DatetimeIndex(df_schedule['Time']).day
    df_schedule['Month'] = pd.DatetimeIndex(df_schedule['Time']).month
    df_schedule['Year'] = pd.DatetimeIndex(df_schedule['Time']).year
    df_schedule['week_number'] = df_schedule['Time'].dt.week
    ##################################Save data of user book to data base ##############################
    filename = "User_schedule.csv"
    df_schedule.to_csv(filename, index=False)
    df_schedule.drop(['Day', 'Month', 'Year', 'Time'], axis=1, inplace=True)
    # display(df_schedule.head(20))
    df_schedule['Make_Schedule_count_byweek'] = df_schedule.groupby(['week_number', 'Hour'])['Make_Schedule'].transform(
        'sum')
    df_schedule = df_schedule.drop_duplicates(subset=['week_number', 'Hour']).drop('Make_Schedule', 1)
    df_schedule['datetime'] = df_schedule['week_number'].map(str) + '_' + df_schedule['Hour'].map(str)

    df_schedule['index'] = df_schedule.index

    def f(x):
        if (x['Hour'] >= 1) and (x['Hour'] <= 6):
            return "Sleep Time"
        elif x['Hour'] >= 7 and x['Hour'] <= 12:
            return "Morning Time"
        elif x['Hour'] >= 13 and x['Hour'] <= 18:
            return "Afternoon Time"
        else:
            return "Night Time"

    df_schedule['Time_Region'] = df_schedule.apply(f, axis=1)

    df_schedule['Avg. Make_Schedule_count_byweek'] = df_schedule.groupby(['week_number', 'Time_Region'])[
        'Make_Schedule_count_byweek'].transform('mean')

    df_schedule2 = df_schedule.drop(
        ['Hour', 'week_number', 'datetime', 'Time_Region', 'Avg. Make_Schedule_count_byweek'], 1)
    df_schedule2 = df_schedule2.drop('index', 1)
    X = df_schedule2.values

    # split into train and test sets

    size = int(len(X)) - 24
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()

    # evaluate an ARIMA model using a walk-forward validation

    for t in range(len(test)):
        model = ARIMA(history, order=(5, 1, 0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)

    df_update = pd.DataFrame(predictions, columns=['Prediction Number of Booking'])
    df_update['Time'] = df_update.index
    df_update.to_csv('PreditionTable.csv')


    max_value = max(predictions)
    max_index = predictions.index(max_value)

    mx = max(predictions[0], predictions[1])
    second_max_value = min(predictions[0], predictions[1])
    n = len(predictions)
    for i in range(2, n):
        if predictions[i] > mx:
            second_max_value = mx
            mx = predictions[i]
        elif (predictions[i] > second_max_value) and (mx != predictions[i]):
            second_max_value = predictions[i]

    second_max_index = predictions.index(second_max_value)
    result_expected = 'The first priority hour: '+str(max_index)+':00'+'\nThe second priority hour: ' +str(second_max_index)+':00' 
    return render(request,'index.html',{'result': result_expected})