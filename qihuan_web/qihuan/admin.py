from django.contrib import admin
from .models import DevelopProject
# Register your models here.
class DevelopProjectAdmin(admin.ModelAdmin):
	pass

admin.site.register(DevelopProject,DevelopProjectAdmin)