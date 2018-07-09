## 奇幻网站开发过程

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

## 