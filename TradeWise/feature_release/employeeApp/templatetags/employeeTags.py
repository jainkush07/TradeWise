from django import template
from django.template.defaulttags import register

register = template.Library()

@register.inclusion_tag('employee/tempTagHTML/sideMenu.html')
def empScreensSideMenu(slug, pageFlag='personalDetail'):
	context = {
		'slug':slug,
		'pageFlag':pageFlag,
	}
	return context