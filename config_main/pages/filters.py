import django_filters

from .models import *
from django import forms

class Metratr116Filter(django_filters.FilterSet):
	# speed__gt = django_filters.NumberFilter(field_name='speed', lookup_expr='speed__gt')
	# speed__lt = django_filters.NumberFilter(field_name='speed', lookup_expr='speed__lt')

	class Meta:
		# model = Metratr116
		model = Metratr116_reprocessed
		fields = [
		'tr_id',
		'carloc',
		'speed'
		]
		fields = {
			'tr_id':['exact'],
			'carloc':['exact'],
			'speed':['lte','gte']
		}

		
	def __init__(self, *args, **kwargs):
		super(Metratr116Filter, self).__init__(*args, **kwargs)
		self.filters['tr_id'].label="Train Date/Time"
		self.filters['carloc'].label="Vehicle Type"
		# self.filters['speed'].label="Speed"
		self.filters['speed__lte'].label = "Speed (max)"
		self.filters['speed__gte'].label = "Speed (min)"


class CtaTableFilter(django_filters.FilterSet):
	
	class Meta:
		model = Cta_backup
		fields = [
		'train_id',
		'axle',
		'speed',
		'train_num',
		'car_num',
		'run_num'
		]
		fields = {
			'train_id':['exact'],
			'axle':['exact'],
			'speed':['lte','gte'],
			'train_num':['contains'],
			'car_num':['exact'],
			'run_num':['exact']
		}

		widgets = {
         'speed': forms.TextInput(attrs={'type': 'range'})
         }
		
	def __init__(self, *args, **kwargs):
		super(CtaTableFilter, self).__init__(*args, **kwargs)
		self.filters['train_id'].label="Train Date/Time"
		self.filters['axle'].label="Axle Number"
		self.filters['speed__lte'].label = "Speed (max)"
		self.filters['speed__gte'].label = "Speed (min)"
		self.filters['train_num__contains'].label = "Train Number"
		self.filters['car_num'].label = "Car Number"
		self.filters['run_num'].label = "Run Number"