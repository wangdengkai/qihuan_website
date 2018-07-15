# 奇幻人生注册和登录

1     需求:之前已经将个人博客页面搞定,现在我们将要开始新的征程,将用户注册登录实现.

​	 首先创建一个client.app(如何创建请参考之前的步骤),用来管理用户登录者注册功能,目前我们希望用户注册时,要填写名称,密码,邮箱.django本身已经自带这种功能了.所以我们不用定义模型了.

2 编写用户注册表单,

(Django 用户系统内置了登录、修改密码、找回密码等视图，但是唯独用户注册的视图函数没有提供，这一部分需要我们自己来写。Django已经内置了一个用户注册表单,django.contrib.auth.forms.UserCreationForm.我们直接使用就好了.

3 编写用户注册视图函数:

```
views.py
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
		form = UserCreationForm(request,POST)

		if form.is_valid():
			# 表单数据合法,进行其他处理i....
			# 调用表单save方法,将数据保存到数据库
			form.save()
			# 判断是否存在注册之前的页面
			if redirect_to:
				#注册成功返回之前的页面
				return redirect(redirect_to)
			else:
				#注册成功返回到首页
				return redirect('/')

	else:
		# 请求不是post,构造一个空表单,表明用户正在访问注册页面,展示一个空的注册表单
		form = UserCreationForm()
	# 渲染表单,如果不是post,那么渲染的是一个空的表单,如果用户通过表单提交数据,
	# 但是数据验证不合法,则渲染的是一个带有错误信息的表单
	return render(request,'template.html',context={'form':form,'next':redirect_to})
	
```

4	设置url模式

```
在这个app下创建一个urls.py,
client/urls.py

from django.urls import path
from . imrpot  views

app_name='client'
urlpatterns =[
	path('register/',views.qihuan_register,name='register'),
]
在项目根目录下,进行设置.
qihuan_web/urls.py

from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('common/',include('common.urls')),  
    path('blog/common/',include('common.urls')),
    path('search/common/',include('common.urls')),
    path('search/',include('haystack.urls')),
    path('blog/',include('blog.urls')),
    path('client/',include('client.urls')),
    
]
```

5 设置模板

```
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
	<title>注册页面</title>
	<link rel="stylesheet" href="https://unpkg.com/mobi.css/dist/mobi.min.css">
	<style>

		.errorlist{
			color:red;

		}
	</style>
</head>
<body>
<div class="flex-center">
	<div class="container">
		<div class="flex-center">
			<div class="unit-1-2 unit-1-on-mobile">
				<h3>注册</h3>
				<form class="form" action="{% url 'client:register' %}" method="POST">
				{% csrf_token %}
				{% for field in form %}
					{{ field.label_tag }}
					{{ field }}
					{{ field.errors }}
					{% if field.help_text %}
						<p class="help text-small text-muted">
						{{ field.help_text |safe }}</p>
					{% endif %}
				{% endfor %}
				<button type="submit" class="btn btn-primary btn-block">注册</button>
				<input type="hidden" name="next" value="{{ next }}"/>
				 </form>
				<div class="flex-center top-gap text-small">
					<a href="login.html">已有账号登录</a>
				</div>
			</div>
		</div>
	</div>
</div>

```

6 登录,登录相关视图django已经写好,我们只需要简单配置就可以啦.

```
from django.contrib import admin
from django.urls import path, include



urlpatterns = [   
    path('admin/', admin.site.urls),
    path('common/',include('common.urls')),  
    path('blog/common/',include('common.urls')),
    path('search/common/',include('common.urls')),
    path('search/',include('haystack.urls')),
    path('blog/',include('blog.urls')),
    path('client/',include('client.urls')),
    path('users',include('django.contrib.auth.urls')),
    
]
```

7编写登录模板

```
{% load staticfiles %}
<!DOCTYPE html>
<html>
<head>
	<link href="{% static 'blog/css/bootstrap.min.css' %}" rel="stylesheet">
	
	<script type="text/javascript" src="{% static 'blog/js/jquery.min.js' %}"></script>
	<script type="text/javascript" src="{% static 'blog/js/bootstrap.min.js' %}"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
	<title>注册页面</title>

	<style>

		.errorlist{
			color:red;

		}
		
	</style>
</head>
<body>
<div class="container">
	<div class="row">
		<div class="col-md-3 col-md-offset-4">
			<form class="form" action="{% url 'login' %}" method="post">
			{% csrf_token %}
			{{ form.non_field_errors }}
			{% for field in form %}
				{{ field.label_tag }}
				{{ field }}
				{{ field.errors }}
				{% if field.help_text %}
					<p class="help text-small text-muted">{{
					field.help_text|safe }}</p>
					{% endif %}
			{% endfor %}
			<button type="submit" class="btn btn-primary btn-block">登录</button>
			<input type="hidden" name="next" value="{{ next }}"/>			
			</form>
			<div>
				<div><span>没有账号?<a href="{% url 'client:register' %}?next={{ request.path }}">立即注册</a></span></div>
				<div><span><a href="{% url 'password_reset' %}">忘记密码?</a></span></div>
			</div>

		</div>
	</div>
</div>
</body>
</html>

```

8 