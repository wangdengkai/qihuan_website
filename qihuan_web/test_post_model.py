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
		p2 = Post(title="GIL",summary="GIL全局锁,仅仅存在于Cpython编辑器,和python语言没有关系",body="GIL的存在历史原因,解决办法...",author="玄锷无梦",create_time="2018-6-10 7:22:22",modify_time="2018-7-22 18:18:22")
		p2.save()
		p3 = Post.objects.create(title="Linux笔记",summary="这里仅仅收录了常用的linux命令",body="多多使用几次就熟练了...",author="玄锷无梦",create_time="2018-8-8 18:00:00",modify_time="2019-02-03 16:22:00")
		p4 = Post.objects.create(title="元类",summary="元类就是创建类对象的类",author="玄锷无梦",body="python中一切皆对象....",create_time="2018-8-8 19:22:33",modify_time="2018-12-13 00:00:00")
		p5 = Post(title="感恩新时代")
		p5.summary="进入新时代,应当以历史的角度,看待这一历史巨变"
		p5.body="新时代,新历史,新征程..."
		p5.author="玄锷无梦"
		p5.create_time="2017-12-12 00:00:00"
		p5.modify_time="2017-12-12 00:00:00"
		p6 = Post.objects.get_or_create(title="面向对象四大特征",summary="面向对象的抽象,继承,封装,多态",body="面向对象的思想.....",author="玄锷无梦",create_time="2018-7-3 7:12:38",modify_time="2018-7-3 7:12:38")
		P7 = Post.objects.get_or_create(title="ORM对象映射数据库",summary="将对象与数据库关联起来,无需直接操作数据库",body="ORM的定义,原因,使用场景.....",author="玄锷无梦",create_tiem="2018-8-8 00:00:00",modify_time="2019-09-09 12:22:33")
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