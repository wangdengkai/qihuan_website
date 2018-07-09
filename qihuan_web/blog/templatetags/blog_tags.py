from ..models import Post,Category,Mark
from django import template
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_category():
	return Category.objects.annotate(num_post=Count("post")).filter(num_post__gt=0)

@register.simple_tag
def get_mark():
	return Mark.objects.annotate(num_post=Count("post")).filter(num_post__gt=0)