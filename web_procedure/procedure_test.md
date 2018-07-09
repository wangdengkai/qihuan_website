# 奇幻网站开发

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