from django import template
from ..models import blogVideos

register = template.Library()


@register.inclusion_tag('templateTagsHTML/videoBlog/search.html')
def searchVideoTag():
	pass