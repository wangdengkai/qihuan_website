# 			奇幻网站开发过程

## 第一章 搭建环境

1	在本地电脑上创建一个项目文件夹:qihuan_website

2 	github创建项目,名为qihuan_website,然后将项目clone到本地文件夹qihuan_website.

​	如何克隆,参考 廖雪峰Git教程:https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000

3 	创建本地虚拟环境:

​	我使用的是window7电脑,本机安装了python3.		

​		3.1 cmd命令行切换到该文件夹下创建虚拟环境python3_venv:

​			$ python -m venv python3_venv	

​			结果是在当前文件夹下生成一个文件夹python3_venv

​		3. 2	切换到虚拟环境的scripts中,激活虚拟环境	

​			$cd python3_venv/scritps

​			$ activate

​		3.3     命令行首出现(python3_venv)表示虚拟环境激活了.

​		3.4	切换到qihuan_website项目中

​			$ cd ../../qihaun_website

4	安装django

​	$ pip  install  django

​	查看django版本,

​		

```
		#首先进入python环境
		$python
		#导入django
		>>>import django
		#查看django版本
		>>>print(django.get_version())
		2.0.7
		#退出python命令行
		>>> exit()
		
```

5	创建一个django项目		

​	$django-admin   startproject	qihuan_web

​	django会自动创建一个文件夹qihuan_web

​	$cd qihuan_web

​	$python manage.py  runserver 

​	用浏览器访问http://127.0.0.1:8000	如果显示页面是有一个大大大的火箭,django欢迎页面说明项目创建成功.

6	打开mysql数据库,创建一个qihuan_db的数据库,来存储数据.(关于数据库的安装请自定百度)

​	$ mysql -u  mysql -p mysql

​	mysql>create database qihuan_db	charset='utf8';

​	#退出mysql

​	mysql>exit

7	创建应用blog,实现博客功能的模块:ctrl+c结束刚才的运行的服务器

​	$ python  manage.py  startapp  blog

​	会在当前文件夹下创建一个blog文件夹

​	打开当前文件夹下qihuan_web下的settings.py进行设置

​	

```
#文件:./qihuan_web/settings.py

-------------安装应用程序---------------------
INSTALLED_APPS = [
	'blog.apps.BlogConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
]
----------------配置数据库--------------------------
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE':'django.db.backends.mysql',#数据库引擎
        'NAME':'qihuan_db',#数据库名称
        'USER':'root',#用户
        'PASSWORD':'mysql',#密码
        'HOST':'',#连接主机地址,本地
        'PORT':'',#端口,默认
    }
}
----------------设置时区,中国时间------------------
USE_TZ = False
TIME_ZONE = 'Asia/Shanghai'
---------------设置中文--------------------
LANGUAGE_CODE = 'zh-Hans'

=================数据库操作需要接口转换==================
文件:./blog/__init__.py

import pymysql
pymysql.install_as_MySQLdb()
```

8	安装pymysql:

​	$ pip  install  pymysql

​	创建数据库迁移:

​	$python manage.py migrate

​	启动服务器看是否是中文了是否设置成功,显示中文欢迎页面.

​	$python manage.py  runserver



## 第二章 模型设计

1	需求分析,目前要先做一个奇幻博客系统.

​	那么就是要能够发布文章,展示文章,先简单实现个人在django后台发布.

​	那么文章就要有一个数据表,有数据表就要有字段,文章的字段标题,摘要,正文,作者,发布时间,修改时间.

​	那么就是会创建一个模型,保存指定的数据.

​	参考资料:Python必会的单元测试框架 —— unittest  https://blog.csdn.net/huilan_same/article/details/52944782



2	实现模型:

​	参考资料:https://www.cnblogs.com/LiCheng-/p/6920900.html

```
编写blog/models.py
from django.db import models

# Create your models here.
class Post(models.Model):
	# title	:文章标题,可变字符串,不可为空
	title = models.CharField(max_length=50,verbose_name="标题")
	# summary	:文章摘要,可变字符串,不可为空
	summary = models.CharField(max_length=50,verbose_name="摘要")
	# body:文章正文
	body = models.TextField(verbose_name="正文")
	# author	:作者,可变字符串,
	author = models.CharField(max_length=15,verbose_name="作者")
	# create_time:创作时间,日期模型,默认为当前时间,不可为空,,以后不可以改变
	create_time = models.DateTimeField(verbose_name="创作时间",auto_now_add=True)
	# modify_time:最后修改时间,默认为创建时间,以后会改变
	modify_time = models.DateTimeField(verbose_name="修改时间",auto_now=True)

	def __str__(self):		
		return self.title

	class Meta:
		verbose_name = "文章信息表"
		ordering=["-modify_time","title"]
	
----------------------------------------------------------------
激活模型,创建数据表.
1	在启动一个cmd窗口,之前的窗口用来测试,不要动,方便使用.这个新的cmd命令行,要先进入虚拟环境,然后切换到项目目录下,也就是E:\Development\qihuan_website\qihuan_website\qihuan_web
2	创建模型生成更改文件
$python manage.py makemigrations blog
结果是在blog/migrations文件夹下面生成一个0001_initial.py,里面的就是下面将要如何创建数据库的代码了,因为后面的根据那个文件来创建数据表.
查看创建表的sql代码
$python manage.py sqlmigrate blog 0001
迁移数据库,创建表
$python  manage.py  migrate
结果会稍微缓慢,因为在操作数据库,最后出现一练串 ok,那就好了,
如果,想要确定,可以去数据库查看.
```

3 交互测试模型:	

```
1 进入交互环境
$python manage.py shell
>>>from blog.models import Post	#导入模型
------------------------------添加数据---------------------------------------
>>>Post.objects.all()	#查看所有的数据
<QuerySet []>
>>>p1 = Post(title="面向对象四大特征",body="面向对象的定义,作用...",summary="面向对象的抽象,继承,封装,多态",author="玄锷无梦")	#创建对象,create_time,modify_time会自												#动生成无需传入
>>>p1.save()  #保存数据到数据库
>>>Post.objects.all()
<QuerySet [Post:面向对象四大特征]>
>>>p11 = Post.objects.get(title="面向对象四大特征")   #获取数据
>>>p11	#查看对象
...
>>>p11.title	#查看标题
>>>p11.create_time  #查看创建时间
>>>p11.modify_time  #查看创建时间
>>>p11.body="面向对象是程序开发的基础概念..."   #修改p11数据
>>>p11.save()   #保存修改
>>>p11.body  #查看修改后的数据
...
>>>p11.modify_time #查看修改后的修改时间
...
>>>p11.create_time  #查看创建时间
...
'''再增加一行数据,自己添加吧.
	p2 = Post(title="GIL",summary="GIL全局锁,仅仅存在于Cpython编辑器,和python语言没有关系",body="GIL的存在历史原因,解决办法...",author="玄锷无梦")
		p2.save()		
'''
>>>p3 = Post.objects.create(title="Linux笔记",summary="这里仅仅收录了常用的linux命令",body="多多使用几次就熟练了...",author="玄锷无梦") #直接创建并保存到数据库
  >>>p4 = Post.objects.create(title="元类",summary="元类就是创建类对象的类",author="玄锷无梦",body="python中一切皆对象....")
  '''  另外一种修改方法,
		p5 = Post(title="感恩新时代")
		p5.summary="进入新时代,应当以历史的角度,看待这一历史巨变"
		p5.body="新时代,新历史,新征程..."
		p5.author="玄锷无梦"
		p5.save()
'''
'''get_or_create()方法,表示如果没有就插入新的,有的话就不插入.返回值是一个元祖.
p6 = Post.objects.get_or_create(title="面向对象四大特征",summary="面向对象的抽象,继承,封装,多态",body="面向对象的思想.....",author="玄锷无梦")
		P7 = Post.objects.get_or_create(title="ORM对象映射数据库",summary="将对象与数据库关联起来,无需直接操作数据库",body="ORM的定义,原因,使用场景.....",author="玄锷无梦")
'''
------------------------修改数据---------------------------------
'''	
		p1 = Post.objects.get(pk=5)
		p1.title="大力发展科技"
		p1.save()
'''
''' update方法直接修改,立即更新到数据库,返回值是1表示成功,返回值是0表示修改失败.同时modify_time并不会更新.
p3 = Post.filter(title="元类").update(summary="python元类文章")
'''
-------------------查询数据---------------------------
'''get()方法查询,不存在时会报错,django文档中也有其他查询方法,用的时候再说呗.
		p1 = Post.objects.get(title="感恩新时代")
		p2 = Post.objects.get(title="面向对象")		
		#根据pk查询
		p3 = Post.objects.get(pk=1)		
		#根据summary查询,获取的是一个列表
		p4 = Post.objects.filter(summary__icontains="抽象")	
		#根据body查询
		p5 = Post.objects.filter(body__icontains="新时代")	
		#根据author查询,判断结果是否为True
		p6 = Post.objects.filter(author="玄锷无梦")	#查询作者是玄锷无梦
		P7 = Post.objects.exclude(author="玄锷无梦") #查询作者不是玄锷无梦的文章
'''
----------------------删除数据-----------------------------------
'''
p1 = Post.objects.get(pk=5).delete()
Post.objects.filter(title="GIL").delete()
'''
还有很多方法,等到需要的时候再查吧,有兴趣的可以去练练

```

4 admin管理后台管理数据

​	

```
1 创建管理员账号
	$python manage.py createsuperuser
	(自己输入要设置账号密码就行啦)
2 注册模型到admin管理后台
	文件:blog/admin.py
	from django.contrib import admin
	from .models import Post
	# Register your models here.
	class PostAdmin(admin.ModelAdmin):
		pass

	admin.site.register(Post,PostAdmin)
3 启动开发服务器
	$python manage.py runserver
4 打开浏览器,输入localhost:8000/admin/
	输入密码后,可以界面形式的操作增删改查.
```

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

## 第五章为每个文章增加分类和标签

1	需求分析:

​	增加文章分类功能,增加文章标签功能,

​	那么分类就是每一个文章有一个类型,如果在文章表格中再增加一行类型字段,也是可以的.

​	但是这样太冗余,而且增加删改分类太麻烦.所以我们在重新建一个表,只有name属性,就是类型名称.那么你要增加类型,只需要修改这个表,很简单.同时为了文章和类别建立关系,因为彼此是1对多的关系,就用外键,外键放在post表中.

​	同时,因为标签要有多个,而每个文章存在多个标签,因此文章和标签是多对多的关系.

2	模型设计:blog/models.py

```
from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=30,verbose_name="类型名")

	def __str__(self):
		return self.name
	class Meta:
		verbose_name = "类型表"

class Mark(models.Model):
	name = models.CharField(max_length=30,verbose_name="标签名")
	def __str__(self):
		return self.name
	class Meta:
		verbose_name="标签表"

class Post(models.Model):
	# title	:文章标题,可变字符串,不可为空
	title = models.CharField(max_length=50,verbose_name="标题")
	# summary	:文章摘要,可变字符串,不可为空
	summary = models.CharField(max_length=50,verbose_name="摘要")
	# body:文章正文
	body = models.TextField(verbose_name="正文")
	# author	:作者,可变字符串,
	author = models.CharField(max_length=15,verbose_name="作者")
	# create_time:创作时间,日期模型,默认为当前时间,不可为空,,以后不可以改变
	create_time = models.DateTimeField(verbose_name="创作时间",auto_now_add=True)
	# modify_time:最后修改时间,默认为创建时间,以后会改变
	modify_time = models.DateTimeField(verbose_name="修改时间",auto_now=True)
	#添加类型属性
	category = models.Foreignkey(Category,verbose_name="文章类型",ondelete=models.CASCADE)
	#添加标签
	marks = models.ManyToManyField(Mark,verbose_name="文章标签",ondelete=models.CASCADE)
	def __str__(self):		
		return self.title

	class Meta:
		verbose_name = "文章信息表"
```

3 迁移到数据库

```
$ python manage.py makemigration
报错:------------------------------------

You are trying to add a non-nullable field 'cate_name' to post without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option: 2
(原因是因为我们的post数据表中已经有数据了,但是category表中没有数据.而我们要进行一对多关联,也就是因为sql的外键约束,post的cate_name的列的值必须是category表中的id的值.此时没有数据,所以报错,
解决方法:1 删除post表中所有数据2为category模型中增加默认值.我们选择第二种方法

cate_name = models.ForeignKey(Category,on_delete=models.CASCADE,default="1",verbose_name="文章类型")
)
再次更新
$ python  manage.py makemigration
```

4 测试:(测试某些属性,方法,如何使用.)	

```
$ python manage.py shell
#导入
$from blog.models import Post,Category,Mark
#为Category和Mark增加一些数据
$Category.objects.create(name="django")
#自己在为分类增加python,js,sql,linux,new等
$m=Mark(name="底层原理")
#自己为标签增加,动态语言,静态语言,面向对象,黑科技,感等等
#查询所有分类
$Category.objects.all()
#查询所有标签
$Mark.objects.all()
#获取一个post对象,pk是主键
$p5=Post.objects.get(pk=5)
#修改p5的 分类属性
$p5.cate_name=Category.objects.get(name="linux")
$dic={"title":"jquery简单使用","summary":"jquery是前端开发的重要工具","body":"jquery本质上是js的一个封装包,只要学会了js,jquery就手到擒来","author":"wangdengkai","cate_name_id":3}
$Post.objects.create(**dic)
#只修改cate_name
$Post.objects.all()[2].cate_name_id=3
#查询属于某个分类的所有文章
$Post.objects.filter(cate_name__name="python")
#查询某个分类下的所有文章,
$Category.objects.get(pk=1).post_set.all() 
#反向查询文章的分类
$Category.objects.filter(post__title="linux笔记")
#为文章增加标签
$m1 =Mark.objects.get(pk=1)
$m2 =Mark.objects.get(pk=2)
$p1=Post.objects.get(pk=1)
$p1.marks_name.add(m1)
$p1.marks_name.add(m2)
#查看标签
$p1.marks_name.all()
#删除标签
$p1.marks_name.remove(m1)
#获取具有某个标签的所有文章
$m1.post_set.all()
```

5 通过admin后台管理使用:

```
$python manage.py runserver
此时进入后台,只有文章信息表,但是修改文章的时候是有分类和标签栏的.
但是我们需要增加修改分类和标签表,那么就要注册到admin中
#修改blog/admin.py文件
from django.contrib import admin
from .models import Post ,Category,Mark
# Register your models here.
class PostAdmin(admin.ModelAdmin):
	pass
class MarkAdmin(admin.ModelAdmin):
	pass
class CategoryAdmin(admin.ModelAdmin):
	pass

admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Mark,MarkAdmin)
现在可以进入localhost:8000/admin进行管理啦.
```

6 修改模板,页面右边增加标签和分类列表.

```
blog/index.html
{% load blog_tags %}
{% block base_right %}	
	{% get_category as cate_list %}
	{% get_mark as mark_list %}
	<ul>
		<li>文章分类</li>
		{% for cate_obj in cate_list %}
			<li><a href="#">{{ cate_obj.name }}({{ cate_obj.post_set.count }} 篇) </a></li>
		{% empty %}
		<li>暂时没有分类</li>
		{% endfor %}
	</ul>

	<ul>

		<li>文章标签</li>
		{% for mark_obj in mark_list %}
			<li><a href="#">{{ mark_obj.name }} ({{ mark_obj.num_post }}篇) </a></li>
		{% empty %}
			<li>暂时没有标签</li>
		{% endfor %}
	</ul>
{% endblock base_right %}
```

7	增加自定义标签(blog中创建一个templatetags包,和models.py在同一级目录)

```
创建一个文件blog_tags.py
from ..models import Post,Category,Mark
from django import template
from django.db.models.aggregates import Count
#创建一个注册对象
register = template.Library()
#注册自定义标签
@register.simple_tag
def get_category():
	return Category.objects.annotate(num_post=Count("post")).filter(num_post__gt=0)

@register.simple_tag
def get_mark():
	return Mark.objects.annotate(num_post=Count("post")).filter(num_post__gt=0)
```

8 运行,查看分类和标签

```
$python manage.py runserver
```

## 第六章显示文章内容

1	目前首页只是显示一个文章,却有很多文章链接,现在需求是点击其中一个链接,中间区域就就显示这篇文章的内容.为了更好的客户体验,我们采用异步请求.

2 	编写视图

```
1 假设,发送过来的异步请求是http://127.0.0.1:8000/blog/detail/<int:pk>
那么urls.py中增加一个处理路径方法
from django.urls import path
from .views import IndexView,PostDetailView
#命令blog命名空间
app_name="blog"
urlpatterns =[
	path(r'',IndexView.as_view(),name="index"),
	path(r'detail/<int:post_pk>/',PostDetailView.as_view(),name="detail")
]
2 视图中处理,因为返回的是详情可以使用DetailView通用视图
from django.views.generic import ListView,DetailView
class PostDetailView(DetailView):
	'''
		返回每一个文章的具体内容
	'''
	model = Post
	template_name="blog/detail.html"
	context_object_name="post"

```

3	编写blog/models.py,为post增加反向路径

```
def get_absolute_url(self):
		return reverse('blog:detail',kwargs={'pk':self.pk})
```

4	编写blog/index.html

```
{% extends "base.html" %}

{% load staticfiles %}

$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});

{% block link %}
	<link rel="stylesheet" href="{% static 'blog/css/index.css' %}"/>
	

	<script>
		$(function(){
			//获取所有标题的a标签
			 var $TitleA=$("#index_left a")
			//获取文章主题对象
			var $PostBody =$("#post_body")
			//获取显示文章标题对象
			var $PostTitle = $("#post_title")
			//为所有a标签绑定点击事件
			// console.log($TitleA)
			$TitleA.click(function(){
				//发送异步请求,
				// console.log($(this))
				//回调函数
				var $Durl = $(this).attr("href")
				var $Title =$(this).text()
				// console.log($Title)
				// console.log($(this).attr('href'))
				$.get(
					$Durl,
					null,
					function(data){
						// console.log(data)
						$PostTitle.text($Title)
						var $show_data=data.split(";")[1]
						// console.log(show_data)
						$PostBody.text($show_data)
					}
					)
				return false
			})
		})
	</script>
{% endblock link %}

{% block base_left %}
	<ul class="nav" id="index_left">
	{% for post in post_list %}		
			<li><a href="{% url 'blog:detail' post.pk %}">{{ post.title }}</a></li>
		
		
	{% empty %}
		<li>暂时没有文章</li>
	{% endfor %}
	</ul>

{% endblock base_left %}

{% block base_center %}
	{% for post in post_list %}
		{% if forloop.first %}
			
					<h5 id="post_title">{{ post.title }} </h5>

					<p id="post_body">{{ post.body|safe}} </p>
				
		{% endif %}

	{% endfor %}
{% endblock base_center %}




{% load blog_tags %}
{% block base_right %}
	{% get_category as cate_list %}
	{% get_mark as mark_list %}
	<ul class="nav navbar-nav" >
		<li class="ul-header"><a href="#">文章分类</a></li>
		{% for cate_obj in cate_list %}
			<li><a href="#">{{ cate_obj.name }}({{ cate_obj.post_set.count }} 篇)</a></li>
		{% empty %}
		<li>暂时没有分类</li>
		{% endfor %}
	</ul>

	<ul class="nav navbar-nav">

		<li class="ul-header"><a href="#">文章标签</a></li>
		{% for mark_obj in mark_list %}
			<li><a href="#">{{ mark_obj.name }} ({{ mark_obj.num_post }}篇) </a></li>
		{% empty %}
			<li>暂时没有标签</li>
		{% endfor %}
	</ul>
{% endblock base_right %}
```

## 第七章显示分页功能

1	需求,每次将文章都全部显示,太多了.所以要增加分页功能,django有个pageinate模块提供了分页的实现.通用视图中已经包含了了分页功能,我们只需要简单设置一下就好了.

2	视图中增加分页功能blog/views.py

```
class IndexView(ListView):
	'''
		博客首页视图,获取文章列表.
	'''
	model =Post
	template_name = "blog/index.html"
	context_object_name = "post_list"
	#指定paginate_by属性后自动开启分页功能,其值代表每一页包含多少篇文章
	paginator_by = 5
```

3 修改模板blog/index.html

```
{% extends "base.html" %}

{% load staticfiles %}

$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});

{% block link %}
	<link rel="stylesheet" href="{% static 'blog/css/index.css' %}"/>
	

	<script>
		$(function(){
			//获取所有标题的a标签
			 var $TitleA=$("#index_left a")
			//获取文章主题对象
			var $PostBody =$("#post_body")
			//获取显示文章标题对象
			var $PostTitle = $("#post_title")
			//为所有a标签绑定点击事件
			// console.log($TitleA)
			$TitleA.click(function(){
				//发送异步请求,
				// console.log($(this))
				//回调函数
				var $Durl = $(this).attr("href")
				var $Title =$(this).text()
				// console.log($Title)
				// console.log($(this).attr('href'))
				$.get(
					$Durl,
					null,
					function(data){
						// console.log(data)
						$PostTitle.text($Title)
						var $show_data=data.split(";")[1]
						// console.log(show_data)
						$PostBody.html($show_data)
					}
					)
				return false
			})
		})
	</script>
{% endblock link %}

{% block base_left %}
	<ul class="nav" id="index_left">
		<li><h5 class="text-center bg-col-FAD bd-rd">所有文章</h5></li>
	{% for post in object_list %}		
			<li><a href="{% url 'blog:detail' post.pk %}">{{ post.title }}</a></li>
		
		
	{% empty %}
		<li>暂时没有文章</li>
	{% endfor %}			
	</ul>
	<ul class="nav navbar-nav ul-border">
		
				{% if is_paginated %}
					{% if page_obj.has_previous %}
						<li  class="f-si bd-rd bg-col-gre "><a class="f-col-r" href="?page={{ page_obj.previous_page_number }}">上一页</a></li>
					{% endif %}
					<li><p class="f-col-b mar-gin" href="#" class="current">第{{ page_obj.number }}页/共{{ paginator.num_pages }}页</p></li>
					{% if page_obj.has_next %}
						<li  class="f-si bd-rd bg-col-gre"><a class="f-col-r" href="?page={{ page_obj.next_page_number }}">下一页</a></li>
					{% endif %}
				{% endif %}
			
	</ul>

{% endblock base_left %}

{% block base_center %}
	{% for post in post_list %}
		{% if forloop.first %}
			
					<h2 id="post_title" class="text-center">{{ post.title }} </h2>

					<p id="post_body">{{ post.body|safe}} </p>
				
		{% endif %}

	{% endfor %}
{% endblock base_center %}




{% load blog_tags %}
{% block base_right %}
	{% get_category as cate_list %}
	{% get_mark as mark_list %}
	<ul class="nav" >
		<li ><h5 class="text-center bg-col-FAD bd-rd">文章分类</h5></li>
		{% for cate_obj in cate_list %}
			<li><a href="#">{{ cate_obj.name }}({{ cate_obj.post_set.count }} 篇)</a></li>
		{% empty %}
		<li>暂时没有分类</li>
		{% endfor %}
	</ul>

	<ul class="nav">

		<li ><h5 class=" text-center bg-col-FAD bd-rd">文章标签</h5></li>
		{% for mark_obj in mark_list %}
			<li><a href="#">{{ mark_obj.name }} ({{ mark_obj.num_post }}篇) </a></li>
		{% empty %}
			<li>暂时没有标签</li>
		{% endfor %}
	</ul>
{% endblock base_right %}
```

## 第 八章支持markdown

 1 安装markdown模块和pygments模块.,下载一个样式包到blog/css中,支持高亮.(我的git中有一个,)

​	pip  install  markdown  

​	pip   install   Pygments

2  将markdown文本渲染成标准的html文本,在视图中编写.blog/biews.py

```
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.generic import ListView,DetailView
from .models import Post

import markdown

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
	#指定paginate_by属性后自动开启分页功能,其值代表每一页包含多少篇文章
	paginate_by = 5
	
class PostDetailView(DetailView):
	'''
		返回每一个文章的具体内容
	'''
	model = Post
	template_name="blog/detail.html"
	context_object_name="post"

	def get_object(self,queryset=None):
		#重写get_object方法,是因为要对post的body进行渲染
		post =super(PostDetailView,self).get_object(queryset=None)
		#通过markdown对post.body进行渲染
		post.body = markdown.markdown(post.body,
								extensions=[
									'markdown.extensions.extra',
									'markdown.extensions.codehilite',
									'markdown.extensions.toc',
								])
		return post
```

3 将模板标记为安全模式,因为django自动为模板转义blog/detail.html

```
$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});
{{ post.body |safe}}
```

4 现在有个问题,因为我们默认打开每一页的第一篇文章,他是在首页视图中处理的,没有经过markdown渲染,因此跟尴尬,每一次打开和翻页的时候,他都没有渲染.所以为了渲染,每次打开新的网页或者新的一页我们就立马用js请求文章内容.

所以修改index.html中的js代码

```
<script>
		$(function(){
			//获取所有标题的a标签
			 var $TitleA=$("#index_left a")
			//获取文章主题对象
			var $PostBody =$("#post_body")
			//获取显示文章标题对象
			var $PostTitle = $("#post_title")
			//为所有a标签绑定点击事件
			// console.log($TitleA[0])
			
			$TitleA.click(function(){
				//发送异步请求,
				// console.log($(this))
				//回调函数
				var $Durl = $(this).attr("href")
				var $Title =$(this).text()
				// console.log($Title)
				// console.log($(this).attr('href'))
				$.get(
					$Durl,
					null,
					function(data){
						// console.log(data)
						$PostTitle.text($Title)
						var $show_data=data.split(";")[1]
						// console.log(show_data)
						$PostBody.html($show_data)
					}
					)
				return false
			})

			var $first=$("#index_left a:eq(0)")
			console.log($first.attr('href'))
			$.get(
					$first.attr('href'),
					null,					
					function(data){
						console.log(data)
						$PostTitle.text($first.text())
						var $show_data=data.split(";")[1]
						// // console.log(show_data)
						$PostBody.html($show_data)
					}
				)
		})
	</script>
```



## 第九章自动生成摘要

1 需求:现在发现我们的每一篇文章都要手动输入摘要.但是很多情况下,并不需要输入摘要,很烦人,因此,我们让它自动生成摘要.自动生成摘要,是为了提供文章的预览,因此只需要摘取正文之前的N个字符作为摘要就行了.

2 重写save方法,blog/models.py

```
def save(self,*args,**kwargs):
		#如果没有写摘要
		if not self.summary:
			#首先实例化一个markdown类,用来渲染body文本
				md =markdown.Markdown(extensions=[
						'markdown.extensions.extra',
						'markdown.extensions.codehilite',
					])
				self.summary=strip_tags(md.convert(self.body))[:50]
		#调用父类的save方法将数据保存到数据库中
		super(Post,self).save(*args,**kwargs)
```

3 目前在调用save方法时就可以自动生成摘要了.但是在后台admin管理平台中,还是要手动填写.

​	目前暂时不处理这个问题

## 第十章提供搜索功能

1 需求:搜索功能,通过输入关键字从文章的标题,内容,作者中搜索出相关文章在列表左侧显示搜索结果列表.由于自己定义搜素功能比较low,我采用django-haystack,django-haystack 是一个专门提供搜索功能的 django 第三方应用，它支持 Solr、Elasticsearch、Whoosh、Xapian 等多种搜索引擎，配合著名的中文自然语言处理库 jieba 分词，就可以为我们的博客提供一个效s果不错的博客文章搜索系统

2  环境配置

```
1 安装依赖包
	pip  install  whoosh
	pip  install  django-haystack
	pip  install   jieba
2 将django haystack 安装到项目中
	blogproject/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    # 其它 app...
    'haystack',
    'blog',
    'comments',
]


--------------------------------------------
并在后面添加以下配置
blogproject/settings.py

HAYSTACK_CONNECTIONS = {
    'default': {
    	#engine  指定使用的搜索引擎,将安装后的whoosh文件夹中的
    	#从你安装的 haystack 中把   lib/sitepackage/haystack/backends/whoosh_backends.py (python环境中寻找)
        文件拷贝到blog/ 下，重命名为 whoosh_cn_backend.py
    	-----------------------------------------------
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',
        #设置索引文件存放的位置,建立索引时会自动创建.
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
#指定如何对搜素结果分页,这里设置为每10项一页
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
#设置为么当有文章更新时,就更新索引.
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
```

3 处理数据

```
1	在blog应用下新建一个search_indexes.py的文件(规定对那个app进行全文检索,就在那个app下面创建一个search_indexes.py文件,这是索引文件提高检索速度.)
2   写入以下代码
--------------------------------------------------------------
from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex,indexes.Indexable):
	text = indexes.CharField(document=True,use_template=True)
	def get_model(self):
		return Post

	def index_queryset(self,using=None):
		return self.get_model().objects.all()
3 创建数据模板
创建数据模板:
	路径:项目名/templates/search/indexes/blog/post_text.txt
	
	#根据这两个字段建立索引,索引的时候会对这两个字段做全文检索匹配,然后将匹配结果排序后返回.
	{{ object.title }}
	{{ object.body }}
4 配置url
qihuan_web/urls.py

urlpatterns = [
    # 其它...
    url(r'^search/', include('haystack.urls')),
]
```

4  修改模板,index.html 让搜索按钮生效,

```
{% extends "base.html" %}

{% load staticfiles %}

$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});

{% block link %}
	<link rel="stylesheet" href="{% static 'blog/css/index.css' %}"/>
	
	{% block send_post %}
	<script>
		$(function(){
			//获取所有标题的a标签
			 var $TitleA=$("#index_left a")
			//获取文章主题对象
			var $PostBody =$("#post_body")
			//获取显示文章标题对象
			var $PostTitle = $("#post_title")
			//为所有a标签绑定点击事件
			// console.log($TitleA[0])
			
			$TitleA.click(function(){
				//发送异步请求,
				// console.log($(this))
				//回调函数
				var $Durl = $(this).attr("href")
				var $Title =$(this).text()
				// console.log($Title)
				// console.log($(this).attr('href'))
				$.get(
					$Durl,
					null,
					function(data){
						// console.log(data)
						$PostTitle.text($Title)
						var $show_data=data.split(";")[1]
						// console.log(show_data)
						$PostBody.html($show_data)
					}
					)
				return false
			})

			var $first=$("#index_left a:eq(0)")
			console.log($first.attr('href'))
			$.get(
					$first.attr('href'),
					null,					
					function(data){
						console.log(data)
						$PostTitle.text($first.text())
						var $show_data=data.split(";")[1]
						// // console.log(show_data)
						$PostBody.html($show_data)
					}
				)
		})
	</script>
	{% endblock send_post %}
{% endblock link %}

{% block base_left %}
	<ul class="nav" id="index_left">
		<li><h5 class="text-center bg-col-FAD bd-rd">所有文章</h5></li>
	{% for post in object_list %}		
			<li><a href="{% url 'blog:detail' post.pk %}">{{ post.title }}</a></li>
		
		
	{% empty %}
		<li>暂时没有文章</li>
	{% endfor %}			
	</ul>
	<ul class="nav navbar-nav ul-border">
		
				{% if is_paginated %}
					{% if page_obj.has_previous %}
						<li  class="f-si bd-rd bg-col-gre "><a class="f-col-r" href="?page={{ page_obj.previous_page_number }}">上一页</a></li>
					{% endif %}
					<li><p class="f-col-b mar-gin" href="#" class="current">第{{ page_obj.number }}页/共{{ paginator.num_pages }}页</p></li>
					{% if page_obj.has_next %}
						<li  class="f-si bd-rd bg-col-gre"><a class="f-col-r" href="?page={{ page_obj.next_page_number }}">下一页</a></li>
					{% endif %}
				{% endif %}
			
	</ul>

{% endblock base_left %}

{% block base_center %}
	{% for post in post_list %}
		{% if forloop.first %}
			
					<h2 id="post_title" class="text-center"></h2><br><br>

					<p id="post_body"></p>
				
		{% endif %}

	{% endfor %}
{% endblock base_center %}




{% load blog_tags %}
{% block base_right %}
	{% get_category as cate_list %}
	{% get_mark as mark_list %}
	<ul class="nav" >
		<li ><h5 class="text-center bg-col-FAD bd-rd">文章分类</h5></li>
		{% for cate_obj in cate_list %}
			<li><a href="#">{{ cate_obj.name }}({{ cate_obj.post_set.count }} 篇)</a></li>
		{% empty %}
		<li>暂时没有分类</li>
		{% endfor %}
	</ul>

	<ul class="nav">

		<li ><h5 class=" text-center bg-col-FAD bd-rd">文章标签</h5></li>
		{% for mark_obj in mark_list %}
			<li><a href="#">{{ mark_obj.name }} ({{ mark_obj.num_post }}篇) </a></li>
		{% empty %}
			<li>暂时没有标签</li>
		{% endfor %}
	</ul>
{% endblock base_right %}
```

5	创建搜索结果显示页面

```
haystack_search 视图函数会将搜索结果传递给模板 templates/search/search.html，因此创建这个模板文件，显示搜索结果
-------------------------------------------------------------------
{% extends "blog/index.html" %}
{% load highlight %} <!--这是为了提供高亮显示的,必须导入-->

{% block send_post %}
	<!-- 采用了异步请求,来显示相关文章-->
	<script>
		$(function(){
			//获取中间块的对象
			var $ShowCen=$("#base_center")
			//获取所有标签的对象
			var $SeaA = $(".sea_ul a")
			console.log($SeaA)
			//发送异步请求
			$SeaA.click(function(){
				var $Surl = $(this).attr('href')
				console.log($Surl)
				$.get(
					$Surl,
					null,
					function(data){
						var $ShowData = data.split(";")[1]
						$ShowCen.html($ShowData)

					}
					)
				return false
			})
		})
	</script>
{% endblock send_post %}



{% block base_left %}
{% if query %}

	<ul class="sea_ul">
		<li><h5>搜索结果</h5></li>
		{% for result in page.object_list %}
			<li><a href="{{ result.object.get_absolute_url }}">
				{% highlight result.object.title with query %}
			</a></li>
			
		{% empty %}
			<li><span>没有搜索到,换个关键词试试</span></li>
		{% endfor %}
	</ul>
	<ul>
	
			{% if page.has_previous %}
				<li><a href="?q={{ query }}&amp;page={{ page.previous_page_number }}">
				上一页</a></li>		

			{% endif %}
			<li><p>第{{ page.number }}页/共{{ paginator.num_pages }}页</p></li>
			{% if page.has_next %}
				<li><a href="?q={{ query }}&amp;page={{ page.next_page_number }}">下一页</a></li>
			{% endif %}
		
	</ul>
{% endif %}
{% endblock base_left %}

{% block base_center %}
	<ul class="sea_ul">
		{% for result in page.object_list %}
			<li>
					<!-- <h5>{{ result.object.title }}</h5> -->
					<h5>{% highlight result.object.title with query %}</h5>
					<p>{% highlight result.object.title with query %}...</p>
					<a href="{% url 'blog:detail' result.object.pk %}">继续阅读</a>
			</li>
		{% empty %}
	
		<h5>没有搜索到相关文章,请修改关键字试试</h5>
	{% endfor %}
	</ul>
	

{% endblock base_center %}
```

6 修改搜索引擎为中文分词

```
从你安装的 haystack 中把 haystack/backends/whoosh_backends.py 文件拷贝到 blog/ 下，重命名为 whoosh_cn_backend.py（之前我们在 settings.py 中 的 HAYSTACK_CONNECTIONS 指定的就是这个文件），然后找到如下一行代码：
----------------------------------------------------------------------------
schema_fields[field_class.index_fieldname] = TEXT(stored=True, analyzer=StemmingAnalyzer(), field_boost=field_class.boost, sortable=True)
--------------------------------------------------------------------
将其修改为:
#要导入这个模块才可以
from jieba.analyse import ChineseAnalyzer

...
#注意先找到这个再修改，而不是直接添加  
schema_fields[field_class.index_fieldname] = TEXT(stored=True, analyzer=ChineseAnalyzer(),field_boost=field_class.boost, sortable=True)  
```

7	建立索引文件

```
运行命令 python manage.py rebuild_index 就可以建立索引文件了。
```

## 第十一章实现点击分类和标签就显示相关的文章

1	每个分类和标签下面都不止有一篇文章,那么就是一找多的方式,将文章找出来.

​	直接在模板中使用obj.post_set.all就可以啦

2   修改模板,增加每个分类和标签连接功能.

```
{% extends "base.html" %}

{% load staticfiles %}

$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});

{% block link %}
	<link rel="stylesheet" href="{% static 'blog/css/index.css' %}"/>
	
	{% block send_post %}
	<script>
		$(function(){
			//获取所有标题的a标签
			 var $TitleA=$(".index_get_post a")
			 console.log($TitleA)
			//获取文章主题对象
			var $PostBody =$("#post_body")
			//获取显示文章标题对象
			var $PostTitle = $("#post_title")
			//为所有a标签绑定点击事件
			// console.log($TitleA[0])
			

			$TitleA.click(function(){
				//发送异步请求,
				// alert($(this))
				//回调函数
				var $Durl = $(this).attr("href")
				var $Title =$(this).text()
				// console.log($Title)
				// console.log($(this).attr('href'))
				$.get(
					$Durl,
					null,
					function(data){
						// console.log(data)
						$PostTitle.text($Title)
						var $show_data=data.split(";")[1]
						// console.log(show_data)
						// alert($show_data)
						var $SeaRes = $("#hide_sea")
						$SeaRes.hide()
						var $show_data=
						$PostBody.html($show_data)
					}
					)
				console.log(false)
				return false
			})
		})
			
	</script>
	{% endblock send_post %}

	{% block init_post %}
	<script type="text/javascript">
			$(function(){
				var $PostTitle = $("#post_title")
				var $PostBody =$("#post_body")
				var $first=$("#index_left a:eq(0)")
			// console.log($first.attr('href'))
			$.get(
					$first.attr('href'),
					null,					
					function(data){
						// console.log(data)
						$PostTitle.text($first.text())
						var $SeaRes = $("#hide_sea")
						$SeaRes.hide()
						var $show_data=data.split(";")[1]
						// // console.log(show_data)
						$PostBody.html($show_data)

					}
				)
			})
		
	</script>
	{% endblock init_post %}
{% endblock link %}

{% block base_left %}
	

	<ul class="nav index_get_post" id="index_left">
		<li><h5 class="text-center bg-col-FAD bd-rd">所有文章</h5></li>
	{% for post in object_list %}		
			<li><a href="{% url 'blog:detail' post.pk %}">{{ post.title }}</a></li>
		
		
	{% empty %}
		<li>暂时没有文章</li>
	{% endfor %}			
	</ul>
	<ul class="nav navbar-nav ul-border getPost">
		
				{% if is_paginated %}
					{% if page_obj.has_previous %}
						<li  class="f-si bd-rd bg-col-gre "><a class="f-col-r" href="?page={{ page_obj.previous_page_number }}">上一页</a></li>
					{% endif %}
					<li><p class="f-col-b mar-gin" href="#" class="current">第{{ page_obj.number }}页/共{{ paginator.num_pages }}页</p></li>
					{% if page_obj.has_next %}
						<li  class="f-si bd-rd bg-col-gre"><a class="f-col-r" href="?page={{ page_obj.next_page_number }}">下一页</a></li>
					{% endif %}
				{% endif %}
			
	</ul>

{% endblock base_left %}

{% block base_center %}
	{% block sea_post %}
	{% endblock sea_post %}
	
	{% for post in post_list %}
		{% if forloop.first %}
			
					<h2 id="post_title" class="text-center"></h2><br><br>

					<p id="post_body"></p>
				
		{% endif %}

	{% endfor %}

{% endblock base_center %}




{% load blog_tags %}
{% block base_right %}
	{% get_category as cate_list %}
	{% get_mark as mark_list %}
	<ul class="nav" >
		<li><h5 class="text-center bg-col-FAD bd-rd">文章分类</h5></li>
		{% for cate_obj in cate_list %}
			<li>
				<div class="dropdown mar-gin-10">
					<button type="button" class="btn dropdown-toggle" data-toggle="dropdown">
					{{ cate_obj.name }} ({{ cate_obj.num_post }}篇) 
						<span class="caret"></span>
					</button>
					<ul class="dropdown-menu index_get_post" role="menu" aria-labelledby="dropdownMark">
						{% for post in cate_obj.post_set.all %}
						<li role="presentation">
							<a role="menuitem" tabindex="-1"
							href="{{ post.get_absolute_url }}">{{ post.title }}</a>
						</li>
						{% endfor %}
					</ul>
				</div>
			</li>
		{% empty %}
		<li>暂时没有分类</li>
		{% endfor %}
	</ul>

	<ul class="nav">

		<li ><h5 class=" text-center bg-col-FAD bd-rd">文章标签</h5></li>
		{% for mark_obj in mark_list %}
			<li>
				<div class="dropdown  mar-gin-10">
					<button type="button" class="btn dropdown-toggle" data-toggle="dropdown">
					{{ mark_obj.name }} ({{ mark_obj.num_post }}篇) 
						<span class="caret"></span>
					</button>
					<ul class="dropdown-menu index_get_post" role="menu" aria-labelledby="dropdownMark">
						{% for post in mark_obj.post_set.all %}
						<li role="presentation">
							<a role="menuitem" tabindex="-1"
							href="{{ post.get_absolute_url }}">{{ post.title }}</a>
						</li>
						{% endfor %}
					</ul>
				</div>
			
			</li>
		{% empty %}
			<li>暂时没有标签</li>
		{% endfor %}
	</ul>
{% endblock base_right %}
```

3 修改搜索结果页面:search.html

```
{% extends "blog/index.html" %}
{% load highlight %}


{% block init_post %}
{% endblock init_post %}

{% block base_left %}
{% if query %}

	<ul class="sea_ul index_get_post ">
		<li><h5>搜索结果</h5></li>
		{% for result in page.object_list %}
			<li><a href="{{ result.object.get_absolute_url }}">
				{% highlight result.object.title with query %}
			</a></li>
			
		{% empty %}
			<li><span>没有搜索到,换个关键词试试</span></li>
		{% endfor %}
	</ul>
	<ul>
	
			{% if page.has_previous %}
				<li><a href="?q={{ query }}&amp;page={{ page.previous_page_number }}">
				上一页</a></li>		

			{% endif %}
			<li><p>第{{ page.number }}页/共{{ paginator.num_pages }}页</p></li>
			{% if page.has_next %}
				<li><a href="?q={{ query }}&amp;page={{ page.next_page_number }}">下一页</a></li>
			{% endif %}
		
	</ul>
{% endif %}
{% endblock base_left %}


{% block sea_post %}
  <div id="hide_sea">
	<ul class="sea_ul  index_get_post">
		{% for result in page.object_list %}
			<li>
					
					<h5>{% highlight result.object.title with query %}</h5>
					<p>{% highlight result.object.title with query %}...</p>
					<a href="{% url 'blog:detail' result.object.pk %}">继续阅读</a>
			</li>
		{% empty %}
	
		<h5>没有搜索到相关文章,请修改关键字试试</h5>
	{% endfor %}
	</ul>
  </div>

  <h2 id="post_title" class="text-center"></h2><br><br>

	<p id="post_body"></p>
{% endblock sea_post %}


```

## 第十二章实现评论功能

1	需求:实现每篇文章加载出来后,底部显示所有已经有的评论,并且提供多级评论的功能.

2      数据库的设计:为了实现多级评论,每一条评论也要关联上一条评论.评论表设计如下

​	

| id    | name   | text | post_id | up_common | create_time |
| ----- | ------ | ---- | ------- | --------- | ----------- |
| 评论的id | 评论人的姓名 | 评论内容 | 评论文章id  | 上一个评论人的id | 评论时间        |

这样就实现了一个自关联的表,构建成了多级评论.

3	创建评论模块,common	

```
$pytho manage.py startapp common
```

4	将创建的模块安装到项目中,

```
#qihuan_web setting.py
INSTALLED_APPS = [
    'common.apps.CommonConfig',
    'haystack',
    

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
]

```

5	常见模型,common.models.py

```
from django.db import models
from django import forms
from django.urls import reverse
# Create your models here.
class Common(models.Model):
	name = models.CharField(max_length=100,verbose_name="名称")
	email = models.EmailField(max_length=255,verbose_name="邮箱")
	text = models.TextField(verbose_name="评论内容")
	create_time = models.DateTimeField(auto_now_add=True)
	
	#评论相关的文章
	post = models.ForeignKey('blog.Post',on_delete=models.CASCADE)   
	#评论者的上一个评论者
	up_common = models.IntegerField(default=0)


	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('common:common_form',kwargs={'post_pk':self.post.pk,'common_pk':self.pk})
	class Meta:
		verbose_name="评论详情表"
		ordering =["-create_time"]
```

6	迁移到数据库

```
$python manage.py makemigrations
$python manage.py migrate
```

7	django提供了表单模块,为了方便,我们使用表单模块,为我们自动创建相关模块

```
#在common目录下,创建一个forms.py文件
-------------------------------------------------------
from django.db import models
from django import forms
from django.urls import reverse
# Create your models here.
class Common(models.Model):
	name = models.CharField(max_length=100,verbose_name="名称")
	email = models.EmailField(max_length=255,verbose_name="邮箱")
	text = models.TextField(verbose_name="评论内容")
	create_time = models.DateTimeField(auto_now_add=True)
	
	#评论相关的文章
	post = models.ForeignKey('blog.Post',on_delete=models.CASCADE)   
	#评论者的上一个评论者,当up_common为0的时候,表示这一条评论是评论的文章,
	#当up_common为其他值的时候,表示评论是评论的其他评论.
	up_common = models.IntegerField(default=0)


	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('common:common_form',kwargs=		   {'post_pk':self.post.pk,'common_pk':self.pk})
	class Meta:
		verbose_name="评论详情表"
		ordering =["-create_time"]
```

8	创建处理视图:目前我们的视图提供三个功能,一个是,获取某个文章的所有评论

一个是获取评论表单,另外一个是提交评论表单.

```
from django.shortcuts import render
from django.shortcuts import get_object_or_404,redirect
from django.http  import JsonResponse,HttpResponse
from django.http import HttpResponseRedirect

from .models import Common
from .forms import CommonForm

from blog.models import Post
# Create your views here.


def post_common_form(request,post_pk,common_pk):
	'''
		获取请求来到的对象,
		1 判断是post还是get请求
		2 post请求就将评论保存到数据库
		3 get请求返回表单
	'''
	#获取post对象
	
	post = get_object_or_404(Post,pk=post_pk)

	# #获取up_common 对象
	

	if request.method == "POST":

		#生成表单对象,
		form = CommonForm(request.POST)
		#判断表单是否有效
		if form.is_valid():
			#用表单对象生成common对象
			common =form.save(commit=False)
			#将评论跟文章关联起来
			common.post=post
			#将评论跟上一位评论者关联起来
			common.up_common=common_pk
		

			#将最终的评论数据保存到数据库,调用模型的save方法
			common.save()
			#重定向到文章详情页,实际上
			# return render(request,"blog/detail.html")
			return JsonResponse({"true":"true","postId":post.pk})
			# return HttpResponse({"true":"true"})
			# return 
		else:
			#检测到数据不合法,重定向到获取表单
			return JsonResponse({"false":"false","postId":post.pk})
			# return HttpResponseRedirect(post)
			# return 
			# return render(request,"blog/detail.html")
	else:
	#不是post请求返会表单
	# return  HttpResponse("hahah")
	# return render(request,"common\common_form.html",{"post":post})
		common=CommonForm()
		context={
			"post":post,
			"form":common,
			"common_pk":common_pk,
		}
		return render(request,"comment/commonform.html",context)
def get_post_common(request,post_pk,common_pk=0):
	'''
		这个函数提供获取文章下所有评论的功能
	'''
	# print("-get----------------------------")
	# //获得post对象
	# p=post_pk
	post = get_object_or_404(Post,pk=post_pk)
	# # post = Post.object.get(pk=post_pk)
	# # # //获得post对象里的所有common
	common_list=post.common_set.all()
	
	
	# # # //对所有common进行封装
	response=iter_common(request,common_list,post_pk,common_pk)	
	

	# return HttpResponse("hhahahah")
	
	
	return HttpResponse(response)

def iter_common(request,common_list,post_pk,common_pk):
	'''
		这个函数提供对取出所有的评论进行构造html的作用.
	'''
	#设置响应初始值
	response="<ul>"
	print(response)
	print("common_list",common_list)
	print("post_pk",post_pk)
	print("common_pk",common_pk)
	# 从commonlist中取出所有的common_pk 等于common的id的对象列表
	common_current_list = common_list.filter(up_common=common_pk)	
	print("common_current_list",common_current_list)

	# 对这个列表进行遍历渲染
	if len(common_current_list) > 0:
		for common in common_current_list:
			#渲染这个common_post
			response +="""
					<li><h5>%s</h5><span>%s</span> </li>
					<li><button type="buttton" data-postid="%s" data-commonid="%s" class="req_common">回复</button>
					<div class="sub_common">
					</div>
					</li>

					"""%(common.name,common.text,post_pk,common.pk)	
			if len(common_list.filter(up_common=common.pk)) > 0:
				response+="<li>"+iter_common(request,common_list,post_pk,common.pk)+"</li>"
		

		
	response+="</ul>"

	return response
	


```

9	配置url

```
#qihuan_web/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('common/',include('common.urls')), 
    #blog/common,是因为我么采取异步请求的方式,那么必然是在blog的页面中获取评论的请求.
    path('blog/common/',include('common.urls')),
    #因为我么也提供了搜索功能,那么就存在在搜索页面中获取评论的需求
    path('search/common/',include('common.urls')),
    path('search/',include('haystack.urls')),
    path('blog/',include('blog.urls')),
    
]

#common/urls.py

from django.urls import path

from .views import post_common_form,get_post_common

app_name="common"
urlpatterns=[
	path('getcommon/<int:post_pk>/',get_post_common,name="post_common"),
		   path('common/<int:post_pk>/<int:common_pk>/',post_common_form,name="common_form"),
]



```

10 表单模板:因为我们要渲染模板将模板渲染过去.,csrf_token是为了提供csrf验证.

提供了自定义字段是为了能够构造出合适的异步请求.

```
#templates/comment/commonform.html

<form action="{% url 'common:common_form' post.pk common_pk %}" method="post" class="id_form" data-commonid="{{ common_pk }}" data-postid="{{ post.pk }}">	
	{% csrf_token %}
	{{ form }}
	<input type="submit" "value="submit" id="subbutton" />
</form>
```

11	由于评论功能的复杂,代码的增多,我们对index.html,search.html进行了优化,与之前的版本有所不同.并且增加了自定义js文件,将index.html本身的js从外界引入了.

```
#index.html

{% extends "base.html" %}

{% load staticfiles %}


$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});
{% block link %}
	<link rel="stylesheet" href="{% static 'blog/css/index.css' %}"/>
	<script type="text/javascript" src="{% static 'blog/js/send_post.js' %}"></script>	


{% endblock link %}

{% block base_left %}
	

	<ul class="nav index_get_post" id="index_left">
		<li><h5 class="text-center bg-col-FAD bd-rd">所有文章</h5></li>
	{% for post in object_list %}	

			<li><a href="{% url 'blog:detail' post.pk %}" data-postid="{{ post.pk }}" data-posttitle="{{ post.title }}">{{ post.title }}</a></li>
		
		
	{% empty %}
		<li>暂时没有文章</li>
	{% endfor %}			
	</ul>
	<ul class="nav navbar-nav ul-border getPost">
		
				{% if is_paginated %}
					{% if page_obj.has_previous %}
						<li  class="f-si bd-rd bg-col-gre "><a class="f-col-r" href="?page={{ page_obj.previous_page_number }}">上一页</a></li>
					{% endif %}
					<li><p class="f-col-b mar-gin" href="#" class="current">第{{ page_obj.number }}页/共{{ paginator.num_pages }}页</p></li>
					{% if page_obj.has_next %}
						<li  class="f-si bd-rd bg-col-gre"><a class="f-col-r" href="?page={{ page_obj.next_page_number }}">下一页</a></li>
					{% endif %}
				{% endif %}
			
	</ul>

{% endblock base_left %}

{% block base_center %}
	{% block sea_post %}
	{% endblock sea_post %}

	{% block index_post %}
	<div id="hide_sea">
		<ul class="sea_ul  index_get_post nav nvabar-nav">
		{% for post in object_list %}	
		
			<li><a href="{% url 'blog:detail' post.pk %}" data-postid="{{ post.pk }}" data-posttitle="{{ post.title }}"><h5 class="text-center">{{ post.title }}</h5></a></li>
					<p>{{ post.summary }}...</p>
					<a  class="flo-l" href="{% url 'blog:detail' post.pk %}"  data-postid="{{ post.pk }}" data-posttitle="{{ post.title }}">继续阅读</a>
					
			</li>
		{% empty %}
	
				
		{% endfor %}
		</ul>
  	</div>

  
	{% endblock index_post %}
	
	
			
	<h2 id="post_title" class="text-center"></h2><br><br>
	<p id="post_body"></p>
	
	
	<div id="get_common">
	</div>
		

{% endblock base_center %}




{% load blog_tags %}
{% block base_right %}
	{% get_category as cate_list %}
	{% get_mark as mark_list %}
	<ul class="nav" >
		<li><h5 class="text-center bg-col-FAD bd-rd">文章分类</h5></li>
		{% for cate_obj in cate_list %}
			<li>
				<div class="dropdown mar-gin-10">
					<button type="button" class="btn dropdown-toggle" data-toggle="dropdown">
					{{ cate_obj.name }} ({{ cate_obj.num_post }}篇) 
						<span class="caret"></span>
					</button>
					<ul class="dropdown-menu index_get_post" role="menu" aria-labelledby="dropdownMark">
						{% for post in cate_obj.post_set.all %}
						<li role="presentation">
							<a role="menuitem" tabindex="-1"
							href="{{ post.get_absolute_url }}" data-postid="{{ post.pk }}" data-posttitle="{{ post.title }}">{{ post.title }}</a>
						</li>
						{% endfor %}
					</ul>
				</div>
			</li>
		{% empty %}
		<li>暂时没有分类</li>
		{% endfor %}
	</ul>

	<ul class="nav">

		<li ><h5 class=" text-center bg-col-FAD bd-rd">文章标签</h5></li>
		{% for mark_obj in mark_list %}
			<li>
				<div class="dropdown  mar-gin-10">
					<button type="button" class="btn dropdown-toggle" data-toggle="dropdown">
					{{ mark_obj.name }} ({{ mark_obj.num_post }}篇) 
						<span class="caret"></span>
					</button>
					<ul class="dropdown-menu index_get_post" role="menu" aria-labelledby="dropdownMark">
						{% for post in mark_obj.post_set.all %}
						<li role="presentation">
							<a role="menuitem" tabindex="-1"
							href="{{ post.get_absolute_url }}" data-postid="{{ post.pk }}" data-posttitle="{{ post.title }}">{{ post.title }}</a>
						</li>
						{% endfor %}
					</ul>
				</div>
			
			</li>
		{% empty %}
			<li>暂时没有标签</li>
		{% endfor %}
	</ul>
{% endblock base_right %}



```

创建一个新的js文件,blog/static/js/send_post.js

```
$(function(){
	//获取所有文章列表
	get_post_detail();	
			
})




function get_post_detail(){
	/*
	这个函数是用来为每一文章的标题绑定一个点击事件,事件结果是返回文章的详情,并且将文章的评论列表和评论表单都自动渲染完成
	采用的方式是异步方式
	 */
	//获取所有标题的a标签
			 var $TitleA=$(".index_get_post a")
			 console.log($TitleA)
			//获取文章主题对象
			var $PostBody =$("#post_body")
			//获取显示文章标题对象
			var $PostTitle = $("#post_title")
			//为所有a标签绑定点击事件
			// console.log($TitleA[0])
			
			//为每一个文章绑定点击事件
			$TitleA.click(function(){
				//发送异步请求,
				// alert($(this))
				//回调函数
				var $Durl = $(this).attr("href")
				console.log($(this))
				var $Title =$(this).data("posttitle")
				console.log("post_title")
				console.log($Title)
				var $PostId = $(this).data("postid")
				console.log($PostId)
				
				// 点击后发送异步请求,获取文章详情
				$.get(
					$Durl,
					null,
					function(data){
						//收到服务器返回的文章内容后,渲染文章内容到页面中
						
						
						$PostTitle.html($Title)
						var $show_data=data				
						var $SeaRes = $("#hide_sea")
						$SeaRes.hide()						
						$PostBody.html($show_data)

						
						//渲染好文章后,立马请求评论,要求渲染评论
					
						get_common_list($PostId)
						//请求文章下面的评论表单
						get_common_form()

					}
					)
				console.log(false)
				return false
			})
}


function get_common_list(post_id){
		/*
		这是为了获取每一个文章下面的评论列表.
		在这里发送异步get请求,获取列表
		接受一个文章的id
		 */
			//获取标签,将评论渲染在其中
			var $GetCommon =$("#get_common")
			//请求url
			var $Url ="/common/getcommon/"+post_id+"/"
			
			//发送异步请求
			$.get(
				$Url,
				null,
				function(data){
					/*
					收到评论数据后,进行渲染到页面中
					 */
					console.log(data)					
					$GetCommon.html(data);
					get_common_form();
					
			})

			

}




//获取评论的表单
function get_common_form()
{
	/*
	这个函数用来获取每个文章下面的评论表单,将其渲染到页面中.
	 */
			//获取评论按钮的对象
			var  $reqCommon = $(".req_common")
			
			//获取表单要渲染到的标签div中
			// var $SubCommon = $(".req_common").next()
			//评论按钮绑定请求事件
			$reqCommon.click
			(function()
			{
				/*
				评论按钮点击后,自动发送get请求到服务器,获取评论表单

				 */
				var $comid = $(this).data("commonid")				

				//请求的url
				var $Myurl = "common/common/"+$(this).data("postid")+"/"+$comid+"/";
				var $SubCommon =$(this).next()
				//发送get请求
				$.get
				(
					$Myurl,
					null,
					function(data)
					{
						/*
						请求表单获取的回调函数
						 */
						//将请求到的表单渲染到页面中,			
						
						$SubCommon.html(data)

						//把刚刚请求到的表单设置成异步submit
						sendForm($SubCommon);
								
					}
				)

			}
			)
}

function sendForm($SubCommon){
	/*
	将表单提交设置为异步方式,并且提交后,自动清空表单,更新评论列表

	 */
	//设置请求对象------------
	var $subObj = {
			"success":function(data){
				//提交成功后的回调函数
				//返回的json字符串可以当做json对象直接使用
				// console.log(data.postId)
				// 调用请求评论列表刷新评论
				// var oRes = eval('('+data+')')
				// console.log(oRes.postId)
				get_common_list(data.postId)
			},
			"error":function(data){
				//提交失败后的回调函数
				console.log("数据提交失败")
				alert("数据提交失败请重新提交")
			},

			
			"clearForm":true,
			"restForm":true,
			"timeout":6000



	}
	//绑定异步请求------------
	$SubCommon.children(".id_form").ajaxForm($subObj);
}

	

				
```

修改detail.html

```

<div>
	<p>{{ post.body |safe}}</p><br>
	<button type="buttton" data-postid="{{ post.pk }}"  data-commonid=0 class="req_common">评论</button>
	<div class="sub_common">
	</div>
<div>
```

修改search.html

```
{% extends "blog/index.html" %}
{% load highlight %}


{% block base_left %}
{% if query %}

	<ul class="sea_ul index_get_post ">
		<li><h5>搜索结果</h5></li>
		{% for result in page.object_list %}
			<li><a href="{{ result.object.get_absolute_url }}" data-postid="{{ result.object.pk }}" data-posttitle="{{ result.object.title }}">
				{% highlight result.object.title with query %}
			</a></li>
			
		{% empty %}
			<li><span>没有搜索到,换个关键词试试</span></li>
		{% endfor %}
	</ul>
	<ul>
	
			{% if page.has_previous %}
				<li><a href="?q={{ query }}&amp;page={{ page.previous_page_number }}">
				上一页</a></li>		

			{% endif %}
			<li><p>第{{ page.number }}页/共{{ paginator.num_pages }}页</p></li>
			{% if page.has_next %}
				<li><a href="?q={{ query }}&amp;page={{ page.next_page_number }}" >下一页</a></li>
			{% endif %}
		
	</ul>
{% endif %}
{% endblock base_left %}


{% block sea_post %}
  <div id="hide_sea">
	<ul class="sea_ul  index_get_post">
		{% for result in page.object_list %}
			<li>
					
					<h5>{% highlight result.object.title with query %}</h5>
					<p>{% highlight result.object.summary with query %}...</p>
					<a href="{% url 'blog:detail' result.object.pk %}"  data-postid="{{ result.object.pk }}" data-posttitle="{{ result.object.title }}">继续阅读</a>
			</li>
		{% empty %}
	
		<h5>没有搜索到相关文章,请修改关键字试试</h5>
	{% endfor %}
	</ul>
  </div>

  <h2 id="post_title" class="text-center"></h2><br><br>

	<p id="post_body"></p>
{% endblock sea_post %}

```

这样我们的伟大的多级评论终于实现了!









==========================最后考虑,先快速开发==============================

2	编写测试

​	2.1  创建测试文件夹:

​	

```
$mkdir test_programmer

$ cd  test_programmer
$mkdir blog_test
```

​	2.2	编写测试文章数据的文件:	

```
	#假设我们的文章模型名字是Post
	#创建测试文件夹
	$cd blog_test
	$touch test_post_model.py
	$touch __init__.py
	
=============编写这个文件  test_post_model.py======================
#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
这个文件用来测试,blog应用中post模型的功能是否正常.
假设模型post具有以下属性:
title	:文章标题,可变字符串,不可为空
summary	:文章摘要,可变字符串,不可为空
body:文章正文
author	:作者,可变字符串,
create_time:创作时间,日期模型,默认为当前时间,不可为空,,以后不可以改变
modify_time:最后修改时间,默认为创建时间,以后会改变

'''
#导入unittest模块
import unittest
#测试创建操作数据库的方法,必须导入TestCase
from  django.test import TestCase




#导入要测试的模型
from  blog.models import Post

#创建测试类
class PostTestCase(TestCase):

	#测试添加数据
	def test_add_post():
		'''
		如何测试数据是否添加成功,
		那么首先必须创建数据对象,并增加后,如果不报错,那么数据添加成功.

		'''
		#创建添加7ge对象,数据库中应当有6条
		p1 = Post(title="面向对象四大特征",body="面向对象的定义,作用...",summary="面向对象的抽象,继承,封装,多态",author="玄锷无梦",create_time="2018-7-3 7:12:38",modify_time="2018-7-3 7:12:38")
		p1.save()
		p2 = Post(title="GIL",summary="GIL全局锁,仅仅存在于Cpython编辑器,和python语言没有关系",body="GIL的存在历史原因,解决办法...",author="玄锷无梦")
		p2.save()
		p3 = Post.objects.create(title="Linux笔记",summary="这里仅仅收录了常用的linux命令",body="多多使用几次就熟练了...",author="玄锷无梦")
		p4 = Post.objects.create(title="元类",summary="元类就是创建类对象的类",author="玄锷无梦",body="python中一切皆对象....")
		p5 = Post(title="感恩新时代")
		p5.summary="进入新时代,应当以历史的角度,看待这一历史巨变"
		p5.body="新时代,新历史,新征程..."
		p5.author="玄锷无梦"
		p5.save()
		p6 = Post.objects.get_or_create(title="面向对象四大特征",summary="面向对象的抽象,继承,封装,多态",body="面向对象的思想.....",author="玄锷无梦")
		P7 = Post.objects.get_or_create(title="ORM对象映射数据库",summary="将对象与数据库关联起来,无需直接操作数据库",body="ORM的定义,原因,使用场景.....",author="玄锷无梦")
		#计算数据库中的数据数量,判断是否正确
		self.assertEqual(Post.objects.all().count(),6)

	#测试查询数据
	def test_select_post():
		#根据title查询
		p1 = Post.objects.get(title="感恩新时代")
		p2 = Post.objects.get(title="面向对象")
		self.assertFalse(p2)
		with self.assertRaises(AttributeError):
			Post.objects.get(title="迎娶白富美")
		#根据pk查询
		p3 = Post.objects.get(pk=1)
		self.assertEqual(p3.title,"面向对象四大特征")
		#根据summary查询,获取的是一个列表
		p4 = Post.objects.filter(summary__icontains="抽象")
		self.assertTrue(instance(p4,set))
		#根据body查询
		p5 = Post.objects.filter(body__icontains="新时代")
		self.assertTrue(instance(p5,set))
		#根据author查询,判断结果是否为True
		p6 = Post.objects.filter(author="玄锷无梦")
		self.assertTrue(instance(p6,set))
		#根据author查询
		P7 = Post.objects.exclude(author="玄锷无梦")
		self.assertFalse(p7)



	#测试修改数据
	def test_modify_post():
		'''
		修改指定字段的值,把它取出来,查看是否修改成功.
		'''
		p1 = Post.objects.get(pk=5)
		p1.title="大力发展科技"
		p1.save()
		p2 = Post.objects.get(pk=5)
		self.assertEqual(p2.title,"大力发展科技")

		p3 = Post.filter(title="元类").update(summary="python元类文章")
		self.assertEqual(Post.filter(title="元类").summary,"python元类文章")
		#测试删除数据
		
	def test_del_post():
		'''
		这是删除,将几条记录进行删除,查询是否还存在
		'''
		p1 = Post.objects.get(pk=5).delete()
		with assertRaises(Exception):
			Post.objects.get(pk=5)




if __name__ == '__main__':
	#运行测试,unittest会自动实例化所有的类,
	#然后运行类中所有以test开头的方法
	unittest.main()
```

​	2.3	为了让测试的输出更好看,更人性化,下载**HTMLTestRunner输出漂亮的HTML报告**			    下载地址https://pan.baidu.com/s/1dEZQ0pz	(请使用这个文档,因为这个是经过修改,适合python3的)

​		创建文件夹

​		

```
		$ cd ..

		$ mkdir  test_html_template

		$ cd test_html_template
		创建一个__init__.py文件
		将下载的模块放到这里.

```



​		

​	2.4 编写主测试文件

​		

```
切换到test programmer
$ cd ..
创建主测试文件test_suite.py

---------------编写test_suite.py---------------------------
import unittest
from test_html_template.HTMLTestRunner import HTMLTestRunner
from blog_test.test_post_model import PostTestCase

if __name__ == '__main__':
	#创建TestSuite对象
	suite = unittest.TestSuite()
	#添加我们的测试类到suite对象中
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PostTestCase))
	#运行测试,输出到测试文档中
	with open('Test_Post_Report.html','w') as f:
		runner = HTMLTestRunner(stream=f,
								title='Blog Post Test Tepost',
								description='generated by HTMLTestRunner.',
								verbosity=2
								)
		runner.run(suite)
```

​	2.5 运行主测试文件:

```
	$ python  test_suite.py
	Traceback (most recent call last):
  	File "test.suite.py", line 3, in <module>
    from blog.test_post_model import PostTestCase
 	 File 			"E:\Development\qihuan_website\qihuan_website\qihuan_web\test_programmer\blog\test_post_model.py", line 24, in <module>
    from  blog.models import Post
ModuleNotFoundError: No module named 'blog.models'
--------------------------------解决办法添加搜索路径-------------------
python添加模块搜索路径和包的导入:
https://blog.csdn.net/weixin_40449300/article/details/79327201
打开虚拟环境python3_venv/Lib/site-packages文件夹
创建一个qihuan_web.pth文件写上你要加入的模块文件所在的文件夹路径
E:\Development\qihuan_website\qihuan_website\qihuan_web
	$ python  test_suite.py
	(出现报错信息,没有post模块)很好,因为我们还没有编写下面就开始边测试边实现吧.

```
## 