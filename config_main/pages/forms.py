from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Metratr116Form(ModelForm):
	class Meta:
		model = Metratr116
		fields = ['tr_id'] ##using all the fields of model "trains_display"




