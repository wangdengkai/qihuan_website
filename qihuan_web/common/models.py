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