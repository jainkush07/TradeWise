from django import template
register = template.Library()

@register.simple_tag()
def multiply(value, multiplier, *args, **kwargs):
	return value * multiplier
