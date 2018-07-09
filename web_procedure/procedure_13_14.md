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

```

