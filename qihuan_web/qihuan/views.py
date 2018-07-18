from django.shortcuts import render
from django.core.mail import BadHeaderError,send_mail
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
def index(request):
	return render(request,'index.html')

def about(request):
	return render(request,'qihuan/about.html')

def reptile(request):
	return render(request,'qihuan/reptile.html')

def intelligence(request):
	return render(request,'qihuan/intelligence.html')

def forum(request):
	return render(request,'qihuan/forum.html')