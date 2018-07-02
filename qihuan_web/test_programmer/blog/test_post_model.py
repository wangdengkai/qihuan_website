#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
这个文件用来测试,blog应用中post模型的功能是否正常.
假设模型post具有以下属性:
title	:文章标题,可变字符串,不可为空
summary	:文章摘要,可变字符串,不可为空
author	:作者,可变字符串,
create_time:创作时间,日期模型,默认为当前时间,不可为空,,以后不可以改变
modify_time:最后修改时间,默认为创建时间,以后会改变

'''
#导入unittest模块
import unittest
#测试创建操作数据库的方法,必须导入TestCase
from  django.test import TestCase

#创建测试类
class PostTestCase(TestCase):
	#测试添加数据
	#测试删除数据
	#测试修改数据
	#测试查询数据





if __name__ == '__main__':
	#运行测试,unittest会自动实例化所有的类,
	#然后运行类中所有以test开头的方法
	unittest.main()