
from django import template
from ..models import blogMedia

register = template.Library()


@register.inclusion_tag('templateTagsHTML/mediaBlog/search.html')
def searchMediaTag():
	pass