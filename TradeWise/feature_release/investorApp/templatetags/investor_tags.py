from django import template
from django.template.defaulttags import register
from ..models import investorPersonalDetails, lookingToInvestDetails, investmentDetails, investorBankDetails, stockBrokerDetails, investorDMATDetails
from django.contrib.auth.models import User
from authNewApp.models import otp_authentication

register = template.Library()

def getProfileCounterView(instProfilOwner):
	field_weight = 100/16.9
	total_weight = 0.0
	try:
		objInst = investorDMATDetails.objects.filter(profileOwner=instProfilOwner).count()
	except:
		objInst = 0
	if objInst > 0:
		total_weight += field_weight
	try:
		objInst = investorBankDetails.objects.filter(profileOwner=instProfilOwner).count()
	except:
		objInst = 0		
	if objInst > 0:
		total_weight += field_weight
	try:
		objInst = investmentDetails.objects.get(profileOwner=instProfilOwner)
		if objInst.presentPortfolio != None:
			total_weight += field_weight
		if objInst.secondaryMarket != None:
			total_weight += field_weight
		if objInst.primaryMarket != None:
			total_weight += field_weight
		if objInst.lookingToInvest != None:
			total_weight += field_weight
		if objInst.secondaryMarket != None:
			total_weight += field_weight
	except:
		objInst = None
	try:
		objInst = investorPersonalDetails.objects.get(profileOwner=instProfilOwner)
		if objInst.name:
			total_weight += field_weight
		if objInst.gender != None:
			total_weight += field_weight
		if objInst.panNumber != None:
			total_weight += field_weight
		if objInst.aadharNumber != None:
			total_weight += field_weight
		if objInst.uploadAadhar != None:
			total_weight += field_weight
		if objInst.address != None:
			total_weight += field_weight
		if objInst.city != None:
			total_weight += field_weight
		if objInst.pinCode != None:
			total_weight += field_weight
		if objInst.country != None:
			total_weight += field_weight
		if objInst.uploadPan != None:
			total_weight += field_weight
	except:
		objInst = None

	roundTotal = int(total_weight)
	return roundTotal

@register.inclusion_tag('tempTagHTML/showAlertPopup.html')
def showAlertTag(request):
	try:
		otpInst = otp_authentication.objects.get(userProfile__pk=request.user.pk)
		user_onboarding = False
		if not otpInst.onboarding_popup:
			user_onboarding = True
			otpInst.onboarding_popup = True
			otpInst.save()
	except:
		user_onboarding = False

	return {
		'request':request,
		'user_onboarding': user_onboarding,
	}

