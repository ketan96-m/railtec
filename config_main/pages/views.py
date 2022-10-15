import imp
import re
from sqlalchemy import create_engine
from django.shortcuts import render, redirect
from django.db.models import Max, Count
from django.db.models.functions import Greatest, Substr
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .decorators import allowed_users

from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.
from django.http import HttpResponse, request
from django.views.generic import View, TemplateView, ListView, UpdateView
import csv
import numpy as np
import pandas as pd
from . import plot1
from .models import *
from django.template import RequestContext
from django.core import serializers
from .forms import Metratr116Form
from .filters import Metratr116Filter



def register_login(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if request.POST.get('submit') == 'sign_up':
            print('Register')
            if form.is_valid():
                form.save()
                user = form.cleaned_data['username']
                print('Account was created',user)
                messages.success(request,"Account was Created for " + user)
                return render(request,'login.html',{'form':form})
            else:
                print('Error', form.errors, request.POST)
                messages.error(request, 'Invalid form submission.')
                messages.error(request, form.errors)
        if request.POST.get('submit') == 'sign_in':
            print('Login attempt')
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print('success', request.POST)
                login(request,user)
                fname = user.first_name
                return redirect('dashboard')
            else:
                messages.error(request, 'Wrong Username or password')
                return render(request,'login.html',{})
    else:
        form = UserCreationForm()
    context = {'form':form}
    return render(request,'login.html',context)
            


class DashboardPageView(TemplateView): 
    template_name = 'dashboard.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DashboardPageView, self).get_context_data(**kwargs)
        
        greatest_v = Metratr116.objects.all().aggregate(largest = Greatest(Max('v1n'), Max('v1s'), Max('v3n'), Max('v3s'))).values()
        great_vert = list(greatest_v)
        great_vert = ','.join(['{:.2f}'.format(x) for x in great_vert])

        # added the separate locomotive and car values
        greatest_v_loc = list(Metratr116.objects.filter(carloc = 'locomotive').aggregate(largest = Greatest(Max('v1n'), Max('v1s'), Max('v3n'), Max('v3s'))).values())
        greatest_v_car = list(Metratr116.objects.filter(carloc = 'car').aggregate(largest = Greatest(Max('v1n'), Max('v1s'), Max('v3n'), Max('v3s'))).values())
        great_vert_loc = round(greatest_v_loc[0], 2)
        great_vert_car = round(greatest_v_car[0], 2)
             

        greatest_l = Metratr116.objects.aggregate(largest = 
            Greatest(Max('l1n'), Max('l1s'))).values()
        great_lat = list(greatest_l)
        great_lat = ','.join(['{:.2f}'.format(y) for y in great_lat])

        TrainsToDate = Metratr116.objects.all().values('tr_id').distinct().count()

        context['plot'] = plot1.cumulative_plot()
        context['great_vert'] = great_vert
        context['great_lat'] = great_lat
        context['TrainsToDate'] = TrainsToDate
        context['great_vert_loc']  = great_vert_loc
        context['great_vert_car']  = great_vert_car
        
        
        return context


class LateralPageView(TemplateView):
    template_name = 'lateral.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LateralPageView, self).get_context_data(**kwargs)
        context['plot'] = plot1.lateral_plot()
        return context

    

class VerticalPageView(TemplateView):
    template_name = 'vertical.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VerticalPageView, self).get_context_data(**kwargs)
        context['plot'] = plot1.vertical_plot()
        return context


def TrainSpecView(request):  
    train_data = Backup_Speed.objects.all()
    return render(request, 'trainspec.html', locals())    


def TrainSpecFilterView(request):
    all_data = Backup_Speed.objects.all()
    myFilter = Metratr116Filter(request.GET, queryset = all_data)
    train_data = myFilter.qs
    context = {'train_data': train_data, 'myFilter' : myFilter}
    return render(request, 'trainspec.html', context)
    
 

def DBTableView(request):
    #data = DummyTable_20220508.objects.all()
    #data = Backup_Speed.objects.order_by('-v1n', '-v1s', '-v3s', '-v3n')[:20]
    #data = Backup_Speed.objects.all().aggregate(Max('v1n'))
    all_fields = [field.name for field in Metratr116._meta.get_fields()[2:3]]
    #get_all = Backup_Speed._meta.get_fields
    datav1n_car = list(Backup_Frontend.objects.filter(carloc = "car").order_by('-v1n')[:4])
    datav1n_loc = list(Backup_Frontend.objects.filter(carloc = "locomotive").order_by('-v1n')[:4])
    datav1s_car = list(Backup_Frontend.objects.filter(carloc = "car").order_by('-v1s')[:4])
    datav1s_loc = list(Backup_Frontend.objects.filter(carloc = "locomotive").order_by('-v1s')[:4])
    datav3n_car = list(Backup_Frontend.objects.filter(carloc = "car").order_by('-v3n')[:4])
    datav3n_loc = list(Backup_Frontend.objects.filter(carloc = "locomotive").order_by('-v3n')[:4])
    datav3s_car = list(Backup_Frontend.objects.filter(carloc = "car").order_by('-v3s')[:4])
    datav3s_loc = list(Backup_Frontend.objects.filter(carloc = "locomotive").order_by('-v3s')[:4])
    context = {
                'all_fields' : all_fields,
                'datav1n_car' : datav1n_car,
                'datav1n_loc' : datav1n_loc,
                'datav1s_car' : datav1s_car,
                'datav1s_loc' : datav1s_loc,
                'datav3n_car' : datav3n_car,
                'datav3n_loc' : datav3n_loc,
                'datav3s_car' : datav3s_car,
                'datav3s_loc' : datav3s_loc,
                }
    return render(request, 'dbtable.html', locals())

@login_required
@allowed_users(allowed_roles=['CTA'])
def testcta(request):    

    context = {}
    return render(request, 'ctadashboard.html', context)


##Separate users for Metra and CTA - 9/24

def enter_view(request):
    if request.user.has_perm('app_label.permission_codename'):
        return redirect('/dashboard')
    elif request.user.has_perm('app_label.another_permission'):
        return redirect('/ctadashboard')
    else:
        return redirect('/dashboard')


