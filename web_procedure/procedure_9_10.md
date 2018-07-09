# 奇幻网站开发过程

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

## 