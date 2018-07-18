from django.db import models

# Create your models here.
class DevelopProject(models.Model):
	#项目名
	pro_name = models.CharField(max_length=50,verbose_name="项目名")
	#项目链接
	pro_href = models.URLField(verbose_name="代码下载地址")
	#项目简单介绍
	pro_info = models.CharField(verbose_name="项目简单介绍",max_length=300)
	#创建时间
	create_time = models.DateTimeField(verbose_name="创建时间")
	#是部署的还是非部署的.默认为False,表示非部署.
	is_run = models.BooleanField(default=False,verbose_name="是部署?")
	#判定类别,人工智能,爬虫,web项目
	CATE_CHOICE ={
		('web','web'),
		('爬虫','爬虫'),
		('人工智能','人工智能'),
	}
	pro_cate = models.CharField(max_length=20,choices=CATE_CHOICE,verbose_name="项目类型")
	#项目小图标
	pro_small = models.ImageField(upload_to="project_img",verbose_name="项目小图标",default=0)

	class Meta:
		ordering = ["-create_time"]
