from django.urls import path
from . import  views

app_name='client'
urlpatterns =[
	
	path('register/',views.qihuan_register,name='register'),
]