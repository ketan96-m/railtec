from django.urls import include, path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', LoginPageView.as_view(), name='login'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    path('lateral/', LateralPageView.as_view(), name='lateral'),
    path('vertical/', VerticalPageView.as_view(), name='vertical'),
    path('dbtable/', views.DBTableView, name = 'dbtable'),
    path('trainspec/', views.TrainSpecView, name = 'trainspec'),
    path('trainspec/<str:train_pk>/', views.TrainSpecFilterView, name = 'trainspec'),
    path('mainscreen/', views.MainScreenView, name = 'mainscreen'),
    
    ]



