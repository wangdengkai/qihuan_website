# 奇幻网站开发过程

## 第三章 模板设计

1 创建文件	

```
在项目根目录下,也就是qihuan_web目录下,创建templates/blog这个目录,
在templates下创建一个文件base.html
```

2 编写基模板templates/base.html

```
<!-- 这是所有页面的基本模板 -->
<!DOCTYPE html>
{% load staticfiles %}    


<html>
<head>	
	<link href="{% static 'blog/css/bootstrap.min.css' %}" rel="stylesheet">
	<sript src="{% static 'blog/js/jquery.min.js' %}"></sript>
	<script src="{% static 'blog/js/bootstrap.min.js' %}"></script>
	<link rel="stylesheet" href="{% static 'blog/css/base.css' %}"/>
	{% block link %} {% endblock link %}
	<title>{% block title %} 奇幻人生{% endblock title %}</title>
	
</head>
<body>
<div id="base_top">
	{% block base_top %}
	<!--===================标题===============================-->

	<div class="container top_title">
		<div class="row">
			<div class="col-xs-12 col-md-12">
				<h1>奇&nbsp;&nbsp;幻&nbsp;&nbsp;人&nbsp;&nbsp;生</h1>
			</div>
		</div>
		<div class="row">
			<div class="col-md-4">
					
					<span>人生如梦,何不放浪形骸</span>
					
			</div>
			<div class="col-md-4">
				<span>奇幻人生,给您不一样的人生</span>
			</div>
			<div class="col-md-4">
				
						<span>生活如山,且须步步为营</span>
							
			</div>
		</div>
		<!--===================导航===============================-->
		<div class="row">
			<div class="col-md-12 col-md-offset-3">
				<nav class="top_nav ">
					<ul class="top_ul nav nav-tabs nav-justified">
						<li class="nav_li"><a href="#">首页</a></li>
						<li class="nav_li"><a href="#">创意</a></li>
						<li class="nav_li"><a href="#">博客</a></li>
						<li class="nav_li"><a href="#">论坛</a></li>
						<li class="nav_li"><a href="#">商城</a></li>
						<li class="nav_li"><a href="#">资源</a></li>
						<li class="nav_li_big">
							<input  class="search" type="text" name="search"/>
							<input  class="button" type="button" name="button" value="搜索">
						</li>
					</ul>
				</nav>
			</div>
	
	</div>
	
	{% endblock base_top %}
	</div>
<div id="base_middle" class="container">
	<div id="base_left" class="row">
		<div class="col-md-2">
			{% block base_left %}

			{% endblock base_left %}
		</div>
	

		<div id="base_center" class="col-md-8">
			{% block base_center %}
			{% endblock base_center %}
		</div>

		<div id="base_right" class="col-md-2">
			{% block base_right %}
			{% endblock base_right %}
		</div>
	</div>
</div>
<div id="base_bottom" class="base_bottom" >
	<div class="row ">
		<div class="col-md-12 ">
			{% block base_bottom %} 
				<div class="row">
					<div class="col-md-2">
					</div>
					<div class="col-md-2 col-md-offset-2">
						<ul class="list-group">
							<li class="list-group-item"><h6 >导航	</h6></li>
							<li class="list-group-item"><a href="#">首页</a></li>					
						</ul>
					</div>
					<div class="col-md-2 ">
						<ul class="list-group">
							<li class="list-group-item"><h6>友情链接</h6></li>
							<li class="list-group-item"><a href=""></a></li>				

						</ul>
					</div>
					<div class="col-md-2 ">
						<ul class="list-group">
							<li class="list-group-item"><h6>产品</h6></li>
							<li class="list-group-item"><a href=""></a></li>
						</ul>
					</div>
					<div class="col-md-2">
						<ul class="list-group">
							<li class="list-group-item"><h6>联系</h6></li>
							<li class="list-group-item"><a href="">地址</a></li>
						</ul>
					</div>
				</div>
				<div class="row">
					<div class="col-md-3"></div>
					<div class="col-md-6">
						<p class="copy_right">Copyright@2018-2035 奇幻人生版权所有</p>
					</div>
					
				</div>
		
			{% endblock base_bottom %}
		</div>

	</div>	
</div>


</body>
</html>
```

3 编写基本的样式base.css(创建blog/static/blog文件夹,将blog所需要的js,imgcss放在这里)

并且将bootstrap样式文件放置在css/文件夹下.

```
*{
	margin:0;
	padding:0;
}
#base_top{
	
	height:80px;	
	
	background-image:url("../images/bg_top_11.jpg");
	background-repeat: repeat-x;
}

#base_top h1{
	text-align: center;
}


span{
	display:inline-block;
	text-align: center;
	
}
.top_nav{
	margin-top:0;
	height:30px;
	background-image:url("../images/nav_bg.png");
}

.top_ul{
	position: relative;
	left:20%;
	
}
li{
	list-style:none;
}
.nav_li{
	float:left;
	list-style:none;
	width:50px;
}

.nav_li_big{
	float:left;
	list-style:none;
}
.button{
	width:50px;

}

.base_middle{
	width:200px;
	height:300px;
	background-color:black;
}
.ul_ul{

}

.base_bottom{
	
	background-color: #F3D4D6;
}
.copy_right{
	padding:0;
	margin:0;
	text-align: center;
	background-color:gray;
}
```

4	添加搜索路径

```
qihuan_web/settings.py
#用于搜索
STATICFIFLES_DIRS=[os.path.join(BASE_DIR,'static'),]
#用于部署nginx
STATIC_ROOT =os.path.join(BASE_DIR,'static')
```

5	编写blog的index.html,(位于qihuan_web/templates/blog/index.html)	

```
{% extends "base.html" %}
{% load static %}

{% block link %}
	<link rel="stylesheet" href="{% static 'css/index.css' %}"/>
{% endblock link %}

{% block base_left %}
	<ul>
	{% for post in post_list %}		
			<li><a href="#">{{ post.title }}</a></li>
		
		
	{% empty %}
		<li>暂时没有文章</li>
	{% endfor %}
	</ul>

{% endblock base_left %}

{% block base_center %}
	{% for post in post_list %}
		{% if forloop.last %}
			
					<h5>{{ post.title }} </h5>

					<p>{{ post.body }} </p>
				
		{% endif %}

	{% endfor %}
{% endblock base_center %}
```

6 编写静态文件blog\static\blog\css\index.css

```
.text-center{
	text-align:center;
}
#base_center p{
	text-indent:25px;
}
.f-si{	
	font-size:20px;
}
.bd-rd{
	border-radius:10px;
}
.bg-col-gre{
	background-color:green;
}
.bg-col-FAD{
	background-color: #FADB96;
}
.f-col-r{
	color:red;
}
.f-col-b{
	color:black;
}
.mar-gin{
	margin:0;
}
```



7  注意事项:

​	  编写每一个模板文件都要加入 {% load staticfiles %}

​	 浏览器查看的时候,注意清除缓存,否则修改后,刷新不会变化.

第四章视图设计

1 编写blog/views.py(采用通用视图ListView)	

```
from django.shortcuts import render

from django.views.generic import ListView,DetailView
from .models import Post
# Create your views here.
'''
使用通用视图
'''
class IndexView(ListView):
	'''
		博客首页视图,获取文章列表.
	'''
	model =Post
	template_name = "blog/index.html"
	context_object_name = "post_list"
```

2配置访问路径:	

```
1 在qihuan_web/blog下面创建一个urls.py文件.进入配置路径
	from django.urls import path
	from .views import IndexView
	#命令blog命名空间
	app_name="blog"
	urlpatterns =[
		path(r'',IndexView.as_view(),name="index"),
	]
2	配置项目qihuan_web\urls.py
	from django.contrib import admin
	from django.urls import path, include

	urlpatterns = [
    	path('admin/', admin.site.urls),
    	#所有blog的请求都交给blog文件夹下urls.py
    	path('blog/',include('blog.urls')), 
	]
```

3 访问浏览器查看:	

```
$ python manage.py runserver
然后浏览器访问
localhost:8000/blog/
基本的流程已经完成,下面都是增加功能进行拓展.
```

## 