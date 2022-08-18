import django_filters

from .models import *

class Metratr116Filter(django_filters.FilterSet):
	class Meta:
		model = Metratr116
		fields = [
		'tr_id',
		'carloc',
		'speed',
		]
		
	def __init__(self, *args, **kwargs):
		super(Metratr116Filter, self).__init__(*args, **kwargs)
		self.filters['tr_id'].label="Train Date/Time"
		self.filters['carloc'].label="Vehicle Type"
		self.filters['speed'].label="Speed"