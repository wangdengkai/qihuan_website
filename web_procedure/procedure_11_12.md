# 			奇幻网站开发过程

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




