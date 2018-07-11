from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.utils.html import strip_tags

from django.http import JsonResponse
from django.http import JsonResponse

from django.core.paginator import Paginator
from django.views.generic import ListView,DetailView



from .models import Post

import markdown

# Create your views here.
'''
使用通用视图
'''
class IndexView(ListView):
	'''
		博客首页视图,获取文章列表.
	'''
	model =Post
	template_name = "blog/index.html"
	context_object_name = "post_list"
	#指定paginate_by属性后自动开启分页功能,其值代表每一页包含多少篇文章
	paginate_by = 5
	
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
		post.save()
		#通过markdown对post.body进行渲染
		post.body = markdown.markdown(post.body,
								extensions=[
									'markdown.extensions.extra',
									'markdown.extensions.codehilite',
									'markdown.extensions.toc',
								])
		return post

    
def Cal_like_number(request,post_id,flag=0):
	'''
		功能:获取和设置点赞数量
		如果flag=0,那么就是获取数量,
		如果flag等于1,那么就是增加点赞数量.
		如果flag等于-1,那么就是减少点赞数量.
	'''
	# 获取文章对象
	post = get_object_or_404(Post,pk=post_id)
	flag = int(flag)
	if flag == 0:
		# //获取点赞数量
		pass
	if flag == 1:
		# //增加点赞数量
		post.like_number +=1
		
	if flag == 2:
		# //减少点赞数量
		post.like_number -=1
		
	post.save()

	return JsonResponse({'like_number':post.like_number})