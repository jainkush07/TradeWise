from django import template
from ..models import blogVideosShorts

register = template.Library()


@register.inclusion_tag('templateTagsHTML/videoShorts/search.html')
def searchShortsTag():
	pass