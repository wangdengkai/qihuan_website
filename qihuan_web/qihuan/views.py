from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request,'index.html')

def contact(request):
	return render(request,'qihuan/contact.html')

def about(request):
	return render(request,'qihuan/about.html')

def reptile(request):
	return render(request,'qihuan/reptile.html')

def intelligence(request):
	return render(request,'qihuan/intelligence.html')

def forum(request):
	return render(request,'qihuan/forum.html')