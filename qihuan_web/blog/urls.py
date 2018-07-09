from django.urls import path,include

from .views import IndexView,PostDetailView
#命令blog命名空间
app_name="blog"
urlpatterns =[
	path('',IndexView.as_view(),name="index"),
	path('detail/<int:pk>/',PostDetailView.as_view(),name="detail"),
	# path('common/',include("common.urls")),
]