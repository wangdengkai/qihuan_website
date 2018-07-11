# 奇幻网站开发

## 第十三章实现文章的阅读数量和评论数量统计,增加点赞功能.

1 需求:统计文章阅读数量,点赞数量,评论数量.

  分析:评论数量,可以根据统计评论表获得.(不管几级评论都算文章评论).

​	阅读数量和点赞数量只有在文章中再增加数字字段来存储了.

​	阅读数量的获取,根据点击进入获取文章detail的操作次数来更改.

​	点赞数量,在文章底部提供一个点赞按钮.来更改点赞.

2 修改post的模型增加两个字段.

```
#blog/models.py
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
	cate_name = models.ForeignKey(Category,on_delete=models.CASCADE,default="1",verbose_name="文章类型")
	#添加标签
	marks_name = models.ManyToManyField(Mark,verbose_name="文章标签")

	#阅读数量
	read_number = models.IntegerField(verbose_name="阅读数量",default=0)
	#点赞数量
	like_number = models.IntegerField(verbose_name="点赞数量",default=0)


	def __str__(self):		
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail',kwargs={'pk':self.pk})

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
	class Meta:
		verbose_name = "文章信息表"
		ordering=["-modify_time","title"]
```

3 迁移到数据库

```
$python manage.py makemigrations
$python manage.py migrate
```

4 修改views.py,当请求一次文章详情的时候,就增加一次文章阅读数量.

```
#blog/views.py
#增加阅读数量
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
		#对post的阅读数量增加
		post.read_number +=1
		pose.save()
		#通过markdown对post.body进行渲染
		post.body = markdown.markdown(post.body,
								extensions=[
									'markdown.extensions.extra',
									'markdown.extensions.codehilite',
									'markdown.extensions.toc',
								])
		return post
```

5 增加点赞处理模块blog/views.py

```
#blog/views.py

def Cal_like_number(post_id,flag=0):
	'''
		功能:获取和设置点赞数量
		如果flag=0,那么就是获取数量,
		如果flag等于1,那么就是增加点赞数量.
		如果flag等于2,那么就是减少点赞数量.
	'''
	# 获取文章对象
	post = get_object_or_404(Post,pk=post_id)
	flag = int(flag)
	if flag == 0:
		//获取点赞数量
		pass
	if flag == 1:
		//增加点赞数量
		post.like_number +=1
	if flag == 2:
		//减少点赞数量
		post.like_number -=1
	post.save()

	return JsonResponse({'post.like_number':post.like_number})
```

6 配置url  blog/urls.py

```
from django.urls import path,include

from .views import IndexView,PostDetailView,Cal_like_number
#命令blog命名空间
app_name="blog"
urlpatterns =[
	path('',IndexView.as_view(),name="index"),
	path('detail/<int:pk>/',PostDetailView.as_view(),name="detail"),
	path('like/<int:post_id>/<int:flag>/',Cal_like_number,name="like"),
	# path('common/',include("common.urls")),
]
```

7 修改detail模板blog/detail.html,增加点赞标签,和阅读数量标签

```
#detail.html

<div>
	<p>阅读数量<span class="read_number">{{ post.read_number }}</span></p>
	<p>{{ post.body |safe}}</p><br>
	<a href="{% url 'blog:like' post.pk  1 %}">点赞数量:{{ post.like_number }}</a>
	<button type="buttton" data-postid="{{ post.pk }}"  data-commonid=0 class="req_common">评论</button>
	<div class="sub_common">

	</div>
<div>
```

8 修改send_post.js文件,点击点赞按钮就可以异步发送请求,增加和减少点赞数量.

```
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

						
						
						// //渲染好文章后,绑定点赞标记
						
						$('#cpostlike').click(get_like_number);
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




function get_like_number(){
		/*
		这个函数用来增加和减少文章的点赞数量
		 */
		
		
	
		//获取标签标记
		var $cNumer = $('#cpostlike')
		
		//判断是增加还是减少点赞数量
		console.log("---------------")
		console.log(like_flag)

		//获取标签本身的url,并构造出请求url
			var $gUrl = $cNumer.prop('href');
		
		if(like_flag == 'false'){
			var reL = new RegExp('/1/');
			console.log(reL)
			
			$gUrl=$gUrl.replace(reL,'/2/');
			console.log($gUrl)
			like_flag = 'true';
		}else{
			//更改flag,实现点击后再次点击可以取消点赞的效果
			like_flag = 'false';

		}	
		
		

		//发送get请求
		$.get(
			$gUrl,
			null,
			function(data){
				$cNumer.text(data.like_number)
			}
		)
	
	//进制冒泡和默认行为
	return false;	

}
```

## 第十四章 整理美化

1 根据个人的爱好,整理整理吧.

