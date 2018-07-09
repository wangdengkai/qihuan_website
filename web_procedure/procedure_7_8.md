# 奇幻网站开发过程

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



## 