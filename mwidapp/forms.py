from django import forms
from django.forms import ModelForm
from .models import *

class AuthorityForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = Authority
		fields = ['username','email','password','mobile','district']


class UserForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = Worker
		fields = ['username','email','password','mobile','district']

class ApplyUserForm(ModelForm):

	class Meta:
		model = Worker
		fields = ['first_name','last_name','gender','address',
		'marital_status','photo','identification_mark','blood_group','uid_aadhar_driv','username','email','mobile',
		'district']