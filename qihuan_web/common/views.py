import datetime
import re
from django.shortcuts import render
from django.shortcuts import get_object_or_404,redirect
from django.http  import JsonResponse,HttpResponse
from django.http import HttpResponseRedirect

from .models import Common
from .forms import CommonForm

from blog.models import Post
# Create your views here.
'''
	目前我们的视图提供三个功能,一个是,获取某个文章的所有评论

一个是获取评论表单,另外一个是提交评论表单.

'''


def post_common_form(request,post_pk,common_pk):
	'''
		获取请求来到的对象,
		1 判断是post还是get请求
		2 post请求就将评论保存到数据库
		3 get请求返回表单
	'''
	#获取post对象
	
	post = get_object_or_404(Post,pk=post_pk)

	# #获取up_common 对象
	
	if request.method == "POST":

		#生成表单对象,
		form = CommonForm(request.POST)
		#判断表单是否有效
		if form.is_valid():
			#用表单对象生成common对象
			common =form.save(commit=False)
			#将评论跟文章关联起来
			common.post=post
			#将评论跟上一位评论者关联起来
			common.up_common=common_pk
		

			#将最终的评论数据保存到数据库,调用模型的save方法
			common.save()
			#重定向到文章详情页,实际上
			# return render(request,"blog/detail.html")
			# return JsonResponse({"true":"true","postId":post.pk})
			# return HttpResponse({"true":"true"})
			return redirect(post)
		else:
			#检测到数据不合法,重定向到获取表单
			return redirect(post)

			# return HttpResponseRedirect(post)
			# return 
			# return render(request,"blog/detail.html")
	else:
	#不是post请求返会表单
	# return  HttpResponse("hahah")
	# return render(request,"common\common_form.html",{"post":post})
		common=CommonForm()
		context={
			"post":post,
			"form":common,
			"common_pk":common_pk,
		}
		return render(request,"comment/commonform.html",context)
def get_post_common(request,post_pk,common_pk=0):
	'''
		这个函数提供获取文章下所有评论的功能
	'''
	# print("-get----------------------------")
	# //获得post对象
	# p=post_pk
	post = get_object_or_404(Post,pk=post_pk)
	# # post = Post.object.get(pk=post_pk)
	# # # //获得post对象里的所有common
	common_list=post.common_set.all()
	
	response='<h2>%s个评论</h2><ol class="commentlist li_s_no">'%len(common_list)
	# # # //对所有common进行封装
	response=iter_common(request,common_list,post_pk,common_pk)+"</ol>"	
	

	
	
	return HttpResponse(response)

def iter_common(request,common_list,post_pk,common_pk):
	'''
		这个函数提供对取出所有的评论进行构造html的作用.
	'''
	#设置响应初始值
	response="<li>"

	# 从commonlist中取出所有的common_pk 等于common的id的对象列表
	common_current_list = common_list.filter(up_common=common_pk)	
	print("common_current_list",common_current_list)

	# 对这个列表进行遍历渲染
	if len(common_current_list) > 0:
		for common in common_current_list:
			# 	time.strptime(str,fmt='%a %b %d %H:%M:%S %Y')
			create_time =common.create_time.strftime("%Y-%m-%d  %H:%M:%S %Y")
			# img_url ="images/content/avatar.gif"
			#渲染这个common_post
			response +="""				

					<div>
	                   
	               		<div>
	               		<h5><span class="f-col-b">%s&nbsp;&nbsp;说:</span></h5> </div>
	                    <div>
	                        <p class="te-ind-20">%s</p>
	                    </div>
	                    	<p class="flo-r">
	                    	<span class="commonTime">时间:%s</span>&nbsp;&nbsp;&nbsp&nbsp;
	                     <a  data-postid="%s" data-commonid="%s" class="req_common">回复</a>
	                     	</p>
	                     <div class="sub_common bg-col-FAD">
						 </div>
						<br/>
	                </div>

					"""%(common.name,common.text,create_time,post_pk,common.pk)	
			if len(common_list.filter(up_common=common.pk)) > 0:
				#迭代,对评论的评论进行封装
				response+='<ol class="li_s_no">'+iter_common(request,common_list,post_pk,common.pk)+"</ol>"
		

		
	response+="</li>"

	return response
	

	
		

