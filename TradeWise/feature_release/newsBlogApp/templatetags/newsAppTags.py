from django import template
from ..models import blogNews

register = template.Library()


@register.inclusion_tag('templateTagsHTML/newsFeed/search.html')
def searchNewsTag():
	pass