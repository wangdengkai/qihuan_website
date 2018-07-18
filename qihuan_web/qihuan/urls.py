from django.urls import path

from . import views 

app_name="qihuan"

urlpatterns=[
	path('',views.index,name="index"),
	
	path('about/',views.about,name="about"),
	path('reptile/',views.reptile,name="reptile"),
	path('intelligence/',views.intelligence,name='intelligence'),
	path('forum/',views.forum,name='forum'),
]