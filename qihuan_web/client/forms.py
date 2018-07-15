from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
	class Meta():
		model = User	
		fileds = ['email','username']
		exclude = ['first_name','last_name','groups','user_permissions','is_staff','is_active','is_superuser','last_login','date_joined','password']


