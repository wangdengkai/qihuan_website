from django.shortcuts import redirect 
from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth import authenticate, login

# Create your views here.


def qihuan_register(request):
	#只有当请求是post时才表示用户提交了注册信息
	#从get或者post请求中获取next参数值,
	#get请求中,next通过url传递,就是/?next=value
	#post请求中,next通过表单传递,就是<input type="hidden" name="next" value="{{ next }}"/>
	redirect_to = request.POST.get('next',request.GET.get('next',''))

	#get请求中,next通过url传递,就是
	# 判断请求类型
	if request.method == 'POST':
		#请求为post,利用用户提交的数据,构造一个绑定了数据的表单
		#这里提交了一个用户名密码和邮箱
		#用这些数据实例化一个用户注册表单
		form = RegisterForm(request.POST)

		       

		if form.is_valid():
			# 表单数据合法,进行其他处理i....
			# 调用表单save方法,将数据保存到数据库
			form.save()

			username = request.POST['username']
			password = request.POST['password1']
			user = authenticate(request,username=username,password=password)
    		

			if user is not None:
				login(request, user)
			

			
			# 判断是否存在注册之前的页面
			if redirect_to:
				#注册成功返回之前的页面
				return redirect(redirect_to)
			else:
				#注册成功返回到首页
				return redirect('/')

	else:
		# 请求不是post,构造一个空表单,表明用户正在访问注册页面,展示一个空的注册表单
	
		form = RegisterForm()
		
	
	# 渲染表单,如果不是post,那么渲染的是一个空的表单,如果用户通过表单提交数据,
	# 但是数据验证不合法,则渲染的是一个带有错误信息的表单
	return render(request,'client/register.html',context={'form':form,'next':redirect_to})
	
		

