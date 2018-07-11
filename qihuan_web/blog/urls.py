from django.urls import path,include

from .views import IndexView,PostDetailView,Cal_like_number
#命令blog命名空间
app_name="blog"
urlpatterns =[
	path('',IndexView.as_view(),name="index"),
	path('detail/<int:pk>/',PostDetailView.as_view(),name="detail"),
	path('like/<int:post_id>/<int:flag>/',Cal_like_number,name="like"),
	
]