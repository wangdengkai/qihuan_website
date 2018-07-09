from django.contrib import admin
from .models import Post ,Category,Mark
import markdown
# Register your models here.
class PostAdmin(admin.ModelAdmin):
	list_display=['title','author','modify_time','cate_name']
	search_fields=['title','author','cate_name','marks_name']
	list_filter=['cate_name','author','marks_name','title']
	ordering=['title','author']
	list_editalbe=['title']
	# date_hierarchy =['moidify_time']
	list_per_page=5

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
class MarkAdmin(admin.ModelAdmin):
	pass
class CategoryAdmin(admin.ModelAdmin):
	pass

admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Mark,MarkAdmin)