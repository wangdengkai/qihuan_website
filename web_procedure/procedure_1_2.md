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

## 





















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