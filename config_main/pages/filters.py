import django_filters

from .models import *

class Metratr116Filter(django_filters.FilterSet):
	# speed__gt = django_filters.NumberFilter(field_name='speed', lookup_expr='speed__gt')
	# speed__lt = django_filters.NumberFilter(field_name='speed', lookup_expr='speed__lt')

	class Meta:
		model = Metratr116
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