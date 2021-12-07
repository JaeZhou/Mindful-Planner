# to-do-list/views.py
from datetime import datetime
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import csv
#from notifications.signals import notify
#from .models import Task

def export_respone(request, choice):
    filename = "User_schedule.csv"
    today = datetime.now()

    make_schedule = 1 if choice=="1" else 0
    current_dt = today.strftime("%y/%m/%d %H:%M:%S")
    current_dt = datetime.strptime(current_dt, "%y/%m/%d %H:%M:%S")
    day = today.day
    month = today.month
    year = today.year
    hour = today.strftime('%H')
    week_num = today.isocalendar().week

    data = [current_dt, hour, make_schedule, day, month, year, week_num]

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
        csvfile.close()

    if make_schedule:
        return HttpResponseRedirect('/timer/')

    else:
        return HttpResponseRedirect('/dashboard/')