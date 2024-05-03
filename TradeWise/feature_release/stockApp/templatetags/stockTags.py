from django import template
from django.template.defaulttags import register
from babel.numbers import format_currency, format_number
from ..models import financialCompanyUpdates, stockTransferDepositoryOptions, saleTypeOptions, stockBasicDetail, researchReportFAQs, commonFAQ, stockEssentials, categoryOptions, welcomeLoginPopup, loginReminderPopup, stockDeckAndDocs
from websiteApp.models import buyPreIPOStockList
from ..peersCrawl import getScreenerPriceForStock
from videoBlogApp.models import blogVideos
from django.contrib.auth.models import User

register = template.Library()

#

@register.inclusion_tag('tempTagHTML/letsBegin.html')
def welcomeLoginTag():
	try:
		popupInst = welcomeLoginPopup.objects.latest('-id')
	except:
		popupInst = None
	# print(f'this is side menu object {popupInst}')
	return {'popupInst':popupInst}


@register.inclusion_tag('tempTagHTML/loginReminderPopup.html')
def reminderLoginTag():
	try:
		sideMenuObj = loginReminderPopup.objects.latest('-id')
	except:
		sideMenuObj = None

	# print(f'this is side menu object {sideMenuObj}')
	return {'sideMenuObj':sideMenuObj}

#
class items_for_pitch_objects:
	def __init__(self, title=None, desc=None, file=None, obj_type=None, video_link=None):
		self.title = title
		self.desc = desc
		self.file = file
		self.obj_type = obj_type
		self.video_link = video_link

	def __str__(self):
		return self.title

#
@register.inclusion_tag('tempTagHTML/new_top_menu_rr.html')
def new_top_menu_rr_tag(request, stock):
	stockDeckAndDocsInst = stockDeckAndDocs.objects.filter(stockProfileName=stock).order_by('-id')
	videos = blogVideos.objects.filter(relatedResearchReports=stock).order_by('-releasedDate')
	pitch_objects = []
	for item in videos:
		for_pitch_obj = items_for_pitch_objects(
				item.title,
				item.subTitle,
				item.blogImage,
				'video',
				item.videoLink,
			)
		pitch_objects.append(for_pitch_obj)
	for item in stockDeckAndDocsInst:
		if item.uploadPDFOrPPT:
			file_ext = item.uploadPDFOrPPT.name.split('.')[-1]
			if file_ext in ['jpeg', 'jpg', 'png',]:
				for_pitch_obj = items_for_pitch_objects(
						item.titleOrYear,
						item.description,
						item.uploadPDFOrPPT,
						'deck'
					)
				pitch_objects.append(for_pitch_obj)
	context = {
		'request': request,
		'stock': stock,
		'pitch_objects': pitch_objects,
	}
	return context

#
@register.inclusion_tag('tempTagHTML/new_side_menu_rr.html')
def new_side_menu_rr_tag(request, stock):
	context = {
		'request': request,
		'stock': stock,
	}
	return context


@register.inclusion_tag('tempTagHTML/annualReports.html')
def annualReportTag():
	pass

#
@register.inclusion_tag('tempTagHTML/messages.html')
def requestMessageTag(messages):
	return {'messages':messages}

#
@register.inclusion_tag('tempTagHTML/leftMenuReports.html')
def leftMenuTag(request, stock):
	return {'request':request,'stock': stock}

#
@register.inclusion_tag('tempTagHTML/mobileMenuReports.html')
def mobileMenuTag(request, stock):
	despositoryOptions = stockTransferDepositoryOptions.objects.all()
	saleType = saleTypeOptions.objects.all()
	return {'request':request,'stock': stock,'despositoryOptions':despositoryOptions, 'saleType':saleType}

#
@register.inclusion_tag('tempTagHTML/rating.html')
def ratingTag(divID, fullStars):
	if not fullStars:
		fullStars = 0
	return {'divID':divID,'fullStars':fullStars}

#
@register.inclusion_tag('tempTagHTML/rightMenuReports.html')
def rightMenuTag(request, stock):
	despositoryOptions = stockTransferDepositoryOptions.objects.all()
	saleType = saleTypeOptions.objects.all()
	return {'request':request,'stock': stock,'despositoryOptions':despositoryOptions, 'saleType':saleType}

@register.inclusion_tag('tempTagHTML/newrightMenuReports.html')
def newrightMenuTag(request, stock):
	despositoryOptions = stockTransferDepositoryOptions.objects.all()
	saleType = saleTypeOptions.objects.all()
	return {'request':request,'stock': stock,'despositoryOptions':despositoryOptions, 'saleType':saleType}

#
@register.inclusion_tag('tempTagHTML/checkListRightMenuReports.html')
def checkListTag(request, stock, visible=True):	
	return {'request':request,'stock': stock, 'visible':visible}

#
@register.inclusion_tag('tempTagHTML/stockFAQs.html')
def stockFAQs(stock, request=None):
	researchReportFAQsInst = researchReportFAQs.objects.filter(stockProfileName=stock).order_by('id')
	commonFAQInst = commonFAQ.objects.all().order_by('id')
	
	context = {
		'request': request,
		'researchReportFAQsInst': researchReportFAQsInst,
		'commonFAQInst': commonFAQInst,
		'stock':stock,
	}
	return context

#
@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)

#
@register.filter
def ownIntComma(value):
	try:
		processedVal = format_currency(value, 'INR', locale='en_IN')
	except:
		processedVal = value
	return processedVal

#
@register.filter
def ownIntCommaWithoutRupees(number):
	processedVal = format_number(number, locale='en_IN')
	return processedVal

#
@register.filter
def roundToTwoPlaces(number):
	processedVal = round(number, 2)
	return processedVal

#
@register.inclusion_tag('tempTagHTML/placeOrderModal.html')
def placeOrderTag():
	pass

#
@register.inclusion_tag('tempTagHTML/placeOrderForm.html')
def placeOrderFormTag(changeID=None, fullHeight=None):
	stockListPreIPO = buyPreIPOStockList.objects.all().order_by('name')
	context = {
		'stockListPreIPO': stockListPreIPO,
		'changeID':changeID,
		'fullHeight':fullHeight,
	}
	return context

#
@register.simple_tag()
def multiply(value, multiplier, *args, **kwargs):
	return value * multiplier

#
def ownIntCommaInternal(value):
	processedVal = format_currency(value, 'INR', locale='en_IN')
	return processedVal

#
@register.simple_tag()
def localOrScreenerPrice(stock, need_int=None):
	stockPrice = ''
	if stock:
		try:
			essentialInst = stockEssentials.objects.get(stockProfileName=stock)
		except:
			essentialInst = None
		screenerPriceCats = categoryOptions.objects.filter(fetchScreenerPrice=True)
		if essentialInst and essentialInst.category in screenerPriceCats:
			stockPrice = getScreenerPriceForStock(essentialInst)
		else:
			try:
				stockPriceInst = buyPreIPOStockList.objects.get(stockName=stock)
				stockPrice = stockPriceInst.investorPrice
			except:
				pass
	if not need_int:
		try:
			stockPrice = ownIntCommaInternal(stockPrice)
		except:
			stockPrice = ''
	return stockPrice


@register.simple_tag()
def checkPassword(request, *args, **kwargs):
	try:
		userInst = User.objects.get(pk=request.user.pk)
	except:
		userInst = None
	try:
		user_have_pass = userInst.has_usable_password()
	except:
		user_have_pass = False
	try:
		user_have_pin = userInst.userProfile_otp_authentication_authV2.login_pin
	except:
		user_have_pin = False
	if user_have_pass and user_have_pin:
		passwordFlag = 'show_both'
	elif not user_have_pass and not user_have_pin:
		passwordFlag = 'no_show'
	elif user_have_pass and not user_have_pin:
		passwordFlag = 'show_pass'
	elif not user_have_pass and user_have_pin:
		passwordFlag = 'show_pin'
	return passwordFlag