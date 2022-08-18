from django.forms import ModelForm
from .models import *

class Metratr116Form(ModelForm):
	class Meta:
		model = Metratr116
		fields = ['tr_id'] ##using all the fields of model "trains_display"
		