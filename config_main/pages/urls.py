from django.urls import include, path
from django.conf.urls import url
from . import views
from .views import *
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',views.register_login, name='login'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    path('lateral/', LateralPageView.as_view(), name='lateral'),
    path('vertical/', VerticalPageView.as_view(), name='vertical'),
    path('dbtable/', views.DBTableView2, name = 'dbtable'),
    path('trainspec/', views.TrainSpecFilterView, name = 'trainspec'),
    path('ctadashboard/', views.testcta, name = 'cta'),
    #path('sign-up/', views.Sign_Up, name = 'sign_up'),
    #path('', LoginPageView.as_view(), name='login'),
    
    
    
    #url(r'^workers/$', login_required(views.as_view()))
    url(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_ROOT}), 
    
    

    ]



