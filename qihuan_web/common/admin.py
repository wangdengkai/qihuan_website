from django.contrib import admin
from .models import Common
# Register your models here.
class CommonAdmin(admin.ModelAdmin):
	list_display=['name','post','create_time','email']
	list_filter = ['post','create_time','name']
	ordering =['post','create_time','name']

admin.site.register(Common,CommonAdmin)
