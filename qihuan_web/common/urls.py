from django.urls import path

from .views import post_common_form,get_post_common

app_name="common"
urlpatterns=[
	path('getcommon/<int:post_pk>/',get_post_common,name="post_common"),
	path('common/<int:post_pk>/<int:common_pk>/',post_common_form,name="common_form"),
]