from django.db import models
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=30,verbose_name="类型名",default="python")

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