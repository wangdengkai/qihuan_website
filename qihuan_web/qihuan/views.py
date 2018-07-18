from django.shortcuts import render
from django.core.mail import BadHeaderError,send_mail
from django.http import HttpResponse,HttpResponseRedirect
from .models import DevelopProject

# Create your views here.
def index(request):
	return render(request,'index.html')

def webproject(request):
	project_list = DevelopProject.objects.all().filter(pro_cate="web",is_run=True)
	#创造一个多重列表[ [],[],[],]
	out_list = []
	inner_list = []
	i = 0
	for project in project_list:
		inner_list.append(project)
		i +=1
		if i == 4:
			i =0
			out_list.append(inner_list)
			inner_list =[ ]
	out_list.append(inner_list)



	context = {
		"project_list":out_list,
	}
	return render(request,'qihuan/web.html',context)

def reptile(request):
	project_list = DevelopProject.objects.all().filter(pro_cate="爬虫",is_run=True)
	#创造一个多重列表[ [],[],[],]
	out_list = []
	inner_list = []
	i = 0
	for project in project_list:
		inner_list.append(project)
		i +=1
		if i == 4:
			i =0
			out_list.append(inner_list)
			inner_list =[ ]
	out_list.append(inner_list)



	context = {
		"project_list":out_list,
	}
	return render(request,'qihuan/reptile.html',context)
def intelligence(request):
	project_list = DevelopProject.objects.all().filter(pro_cate="人工智能",is_run=True)
	#创造一个多重列表[ [],[],[],]
	out_list = []
	inner_list = []
	i = 0
	for project in project_list:
		inner_list.append(project)
		i +=1
		if i == 4:
			i =0
			out_list.append(inner_list)
			inner_list =[ ]
	out_list.append(inner_list)



	context = {
		"project_list":out_list,
	}
	return render(request,'qihuan/intelligence.html',context)



def download(request):
	d_project_list = DevelopProject.objects.all()
	context = {
		"d_project_list":d_project_list,
	}
	return render(request,'qihuan/resource.html',context)