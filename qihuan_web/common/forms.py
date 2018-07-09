from django import forms
from .models import Common

class CommonForm(forms.ModelForm):
	class Meta:
		model = Common
		fileds = ['name','email','text']
		exclude = ['create_time','post','up_common']