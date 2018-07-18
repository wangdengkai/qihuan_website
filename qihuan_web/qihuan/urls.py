from django.urls import path

from . import views 

app_name="qihuan"

urlpatterns=[
	path('',views.index,name="index"),
	path('download/',views.download,name='download'),	
	path('web/',views.webproject,name="web"),
	path('reptile/',views.reptile,name="reptile"),
	path('intelligence/',views.intelligence,name='intelligence'),

]