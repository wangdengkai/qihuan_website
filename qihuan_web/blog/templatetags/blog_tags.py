from ..models import Post,Category,Mark
from django import template
from django.db.models.aggregates import Count
from common.models import Common

register = template.Library()

@register.simple_tag
def get_category():
	return Category.objects.annotate(num_post=Count("post")).filter(num_post__gt=0)

@register.simple_tag
def get_mark():
	return Mark.objects.annotate(num_post=Count("post")).filter(num_post__gt=0)
@register.simple_tag
def recent_post_all(num=3):
	return Post.objects.all()[:num]

@register.simple_tag
def hotspot_post(num=3):
	return Post.objects.annotate(num_post=Count('common')).filter(num_post__gt=0)[:num]
@register.simple_tag
def post_small_img(num):
	img_list = ['qihuan/images/content/post-small1.jpg','qihuan/images/content/post-small2.jpg','qihuan/images/content/post-small3.jpg']
	return img_list[num]

@register.simple_tag
def post_small_left(num):
	img_list=['qihuan/images/content/post_left_small1.jpg','qihuan/images/content/post_left_small2.jpg','qihuan/images/content/post_left_small3.jpg']
	return img_list[num]