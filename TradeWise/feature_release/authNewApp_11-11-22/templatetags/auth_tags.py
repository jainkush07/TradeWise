from django import template
from django.template.defaulttags import register
from authApp.models import loginBannerObjects

#
@register.inclusion_tag('auth_v2/template_tags_html/sidebar_login_screens.html')
def sidebar_auth_screens_tag(request):
	login_type = request.session.get('profile_type') or request.GET.get('type')
	# print('----------SIDEBAR TAG------------')
	# for key, value in request.session.items():
	# 	print(f"{key}:=> {value}")
	# print('----------// SIDEBAR TAG //------------')
	if not login_type:
		login_type = 'INVESTOR'
	try:
		sideMenuObj = loginBannerObjects.objects.get(relatedTo__name=login_type)
	except:
		sideMenuObj = None
	context = {
		'sideMenuObj': sideMenuObj,
	}
	return context

#
@register.inclusion_tag('auth_v2/template_tags_html/otp_verify_modal.html')
def otp_verify_modal_tag(errors):
	context = {
		'errors': errors,
	}
	return context