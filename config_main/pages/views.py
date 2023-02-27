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
from django.urls import reverse_lazy, reverse

# Create your views here.
from django.http import HttpResponse, request, HttpResponseRedirect
from django.views.generic import View, TemplateView, ListView, UpdateView
import csv
import numpy as np
import pandas as pd
from . import plot1, plot2_cta
from .models import *
from django.template import RequestContext
from django.core import serializers
from .forms import Metratr116Form
from .filters import Metratr116Filter, CtaTableFilter
import json
from django.core.paginator import Paginator
import datetime



def register_login(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if request.POST.get('submit') == 'sign_up':
            print('Register')
            if form.is_valid():
                form.save()
                user = form.cleaned_data['username']
                print('Account was created',user)
                messages.success(request,"Account was created for " + user)
                return render(request,'login.html',{'form':form})
            else:
                print('Error', form.errors, request.POST)
                messages.error(request, 'Invalid form submission!')
                messages.error(request, form.errors)
        if request.POST.get('submit') == 'sign_in':
            print('Login attempt')
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    print('success', request.POST)
                    login(request,user)
                    fname = user.first_name
                    return redirect('ctadashboard')
                else:
                    print('ctasuccess', request.POST)
                    login(request,user)
                    fname = user.first_name
                    return redirect('ctadashboard')
            else:
                print("Error", request)
                messages.error(request, 'Wrong Username or Password')
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
    # all_data = Backup_Speed.objects.all()
    all_data = Metratr116_reprocessed.objects.all()
    myFilter = Metratr116Filter(request.GET, queryset = all_data)
    train_data = myFilter.qs
    all_data = False

    # Set the number of entries per page
    paginator = Paginator(train_data, 30)

    # Get the page number from the request's query parameters
    page = request.GET.get('page')

    # Get the specified page from the paginator
    page_entries = paginator.get_page(page)

    for key in myFilter.data.keys():
        if myFilter.data[key] != '':
            all_data = True
            break
    if all_data:
        context = {
            'train_data': page_entries, 
        'myFilter' : myFilter
        }
    else:
        context = {
            'train_data': [], 
        'myFilter' : myFilter
        }
    return render(request, 'trainspec.html', context)


    
 
@login_required
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

    return render(request, 'dbtable.html', context)

@login_required
def DBTableView2(request):
    #data = DummyTable_20220508.objects.all()
    #data = Backup_Speed.objects.order_by('-v1n', '-v1s', '-v3s', '-v3n')[:20]
    #data = Backup_Speed.objects.all().aggregate(Max('v1n'))
    all_fields = [field.name for field in Metratr116_reprocessed._meta.get_fields()[2:3]]
    #get_all = Backup_Speed._meta.get_fields
    top_20_data = []
    top_20_data.extend(list(Metratr116_reprocessed.objects.values_list('tr_id','v1n','speed','carloc').filter(carloc = 'locomotive').order_by('-v1n')[:20]))
    top_20_data.extend(list(Metratr116_reprocessed.objects.values_list('tr_id','v1s','speed','carloc').filter(carloc = 'locomotive').order_by('-v1s')[:20]))
    top_20_data.extend(list(Metratr116_reprocessed.objects.values_list('tr_id','v2s','speed','carloc').filter(carloc = 'locomotive').order_by('-v2s')[:20]))
    
    top_20_data_car = []
    top_20_data_car.extend(list(Metratr116_reprocessed.objects.values_list('tr_id','v1n','speed','carloc').filter(carloc = 'car').order_by('-v1n')[:20]))
    top_20_data_car.extend(list(Metratr116_reprocessed.objects.values_list('tr_id','v1s','speed','carloc').filter(carloc = 'car').order_by('-v1s')[:20]))
    top_20_data_car.extend(list(Metratr116_reprocessed.objects.values_list('tr_id','v2s','speed','carloc').filter(carloc = 'car').order_by('-v2s')[:20]))
    


    df = pd.DataFrame(top_20_data)
    # df[4] = 20*['V1N'] + 20*['V1S'] + 20*['V3N'] +20*['V3S']
    df[4] = 20*['V1N'] + 20*['V1S'] + 20*['V2S']
    df = df.sort_values(1, ascending=False)

    json_records = df.reset_index().to_json(orient ='records')
    datav1n = []
    datav1n = json.loads(json_records)[:20]

    df1 = pd.DataFrame(top_20_data_car)
    df1[4] = 20*['V1N'] + 20*['V1S'] + 20*['V2S']
    df1 = df1.sort_values(1, ascending=False)

    json_records = df1.reset_index().to_json(orient ='records')
    datav1n_car = []
    datav1n_car = json.loads(json_records)[:20]

    # datav1n = sorted(top_20_data, key = lambda x: x[1], reverse=True)[:20]
    # print(Backup_Frontend.objects.values_list('tr_id','v1n','speed','carloc').filter().order_by('-v1n')[:20])
    # print(len(datav1n))
    context = {
                'all_fields' : all_fields,
                'datav1n':datav1n,
                'datav1n_car':datav1n_car
                }
    # return render(request, 'dbtable.html', locals())
    return render(request, 'dbtable.html',context)

# @login_required
class CTADashboard(TemplateView): 
    template_name = 'ctadashboard.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CTADashboard, self).get_context_data(**kwargs)
        
        context['plotcta'] = plot2_cta.cumulative_cta()
        return context

@login_required
def TrainSpecCTA(request):
    all_data = Cta_backup.objects.all()
    myFilter = CtaTableFilter(request.GET, queryset = all_data)
    train_data = myFilter.qs

    # Set the number of entries per page
    paginator = Paginator(train_data, 30)

    # Get the page number from the request's query parameters
    page = request.GET.get('page')

    # Get the specified page from the paginator
    page_entries = paginator.get_page(page)

    context = {'train_data': page_entries, #train_data, 
    'myFilter' : myFilter}
    return render(request, 'ctatrainspec.html', context)

def ExportCSV(request):
    all_data = Cta_backup.objects.all()
    myFilter = CtaTableFilter(request.GET, queryset = all_data)
    train_data = pd.DataFrame(myFilter.qs.values())
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{datetime.datetime.now()}.csv"'
    train_data.to_csv(response, columns = [
        "car_num",	"run_num",	"axle",	"train_id",	
        "speed"	,"l2w"	,"l2e"	,"l1w"	,"l1e"	,"v2w"	,"v2e"	,"v1w"	,"v1e"	,"train_num"
    ], index = False)
    return response


@login_required
def CTADBTable(request):
    
    all_fields = [field.name for field in Cta_backup._meta.get_fields()[2:3]]
    
    datav1e = list(Cta_backup.objects.order_by('-v1e')[:3])
    datav1w = list(Cta_backup.objects.order_by('-v1w')[:3])
    datav2e = list(Cta_backup.objects.order_by('-v2e')[:3])
    datav2w = list(Cta_backup.objects.order_by('-v2w')[:3])
    datal1e = list(Cta_backup.objects.order_by('-l1e')[:3])
    datal1w = list(Cta_backup.objects.order_by('-l1w')[:3])
    datal2e = list(Cta_backup.objects.order_by('-l2e')[:3])
    datal2w = list(Cta_backup.objects.order_by('-l2w')[:3])
    context = {
                'all_fields' : all_fields,
                'datav1e': datav1e,
                'datav1w': datav1w,
                'datav2e': datav2e,
                'datav2w': datav2w,
                'datal1e': datal1e,
                'datal1w': datal1w,
                'datal2e': datal2e,
                'datal2w': datal2w,
                }
    return render(request, 'ctadbtable.html', locals())
    


