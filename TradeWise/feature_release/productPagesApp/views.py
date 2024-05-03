from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from employeeApp.models import country
from stockApp.models import stockBasicDetail, stockEssentials

# Create your views here.

def deleteFKdataView(request):
	if request.method == 'POST':
		deletePK = request.POST.get('deleteDataID')
		deleteFrom = request.POST.get('deleteFlag')
		requestedPage = request.POST.get('redirectTo')

		if deleteFrom =='seedFundingFAQs':
			try:
				objInst = seedFundingFAQs.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='seedFundingPackages':
			try:
				objInst = seedFundingPackages.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='growthFundingFAQs':
			try:
				objInst = growthFundingFAQs.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='growthFundingPackages':
			try:
				objInst = growthFundingPackages.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='earlyFundingFAQs':
			try:
				objInst = earlyFundingFAQs.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='earlyFundingPackages':
			try:
				objInst = earlyFundingPackages.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='seedFundingContactUsKnowMoreFAQs':
			try:
				objInst = seedFundingContactUsKnowMoreFAQs.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='growthFundingContactUsKnowMoreFAQs':
			try:
				objInst = growthFundingContactUsKnowMoreFAQs.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='earlyFundingContactUsKnowMoreFAQs':
			try:
				objInst = earlyFundingContactUsKnowMoreFAQs.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')
		elif deleteFrom =='sellESOPCards':
			try:
				objInst = sellESOPCards.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='sellESOPFAQs':
			try:
				objInst = sellESOPFAQs.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='sellESOPRunningNumbers':
			try:
				objInst = sellESOPRunningNumbers.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='sellESOPContactUsKnowMoreFAQs':
			try:
				objInst = sellESOPContactUsKnowMoreFAQs.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='sellYourStartupExposure':
			try:
				objInst = sellYourStartupExposure.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='sellYourStartupFAQs':
			try:
				objInst = sellYourStartupFAQs.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='sellYourStartupContactUsKnowMoreFAQs':
			try:
				objInst = sellYourStartupContactUsKnowMoreFAQs.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='privateBoutiqueRunningCards':
			try:
				objInst = privateBoutiqueRunningCards.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='privateBoutiqueInvestingProcessCards':
			try:
				objInst = privateBoutiqueInvestingProcessCards.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='privateBoutiqueSellingProcessCards':
			try:
				objInst = privateBoutiqueSellingProcessCards.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='privateBoutiqueWhyToInvestCards':
			try:
				objInst = privateBoutiqueWhyToInvestCards.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='privateBoutiqueContactUsKnowMoreFAQs':
			try:
				objInst = privateBoutiqueContactUsKnowMoreFAQs.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		
		elif deleteFrom =='privateBoutiqueSuccessStories':
			try:
				objInst = privateBoutiqueSuccessStories.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')
		elif deleteFrom =='privateBoutiqueCategory':
			try:
				objInst = privateBoutiqueCategory.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='privateBoutiqueFAQNRI':
			try:
				objInst = privateBoutiqueFAQNRI.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='privateBoutiqueFAQLegality':
			try:
				objInst = privateBoutiqueFAQLegality.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='privateBoutiqueFAQTaxImplications':
			try:
				objInst = privateBoutiqueFAQTaxImplications.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')

		elif deleteFrom =='privateBoutiqueFAQInvestment':
			try:
				objInst = privateBoutiqueFAQInvestment.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')
		return redirect(requestedPage)
	return HttpResponse('Invalid Entry Point')

def seedFundingDMView(request):
	if request.method == 'POST':
		try:
			obj = seedFundingDM.objects.latest('id')
		except:
			obj = None
		objForm = seedFundingDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:seedFundingUrl')
	return HttpResponse('Invalid Entry')

def seedFundingContactDMView(request):
	if request.method == 'POST':
		try:
			obj = seedFundingContactDM.objects.latest('id')
		except:
			obj = None
		objForm = seedFundingContactDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:seedFundingContactUrl')
	return HttpResponse('Invalid Entry')

def growthFundingDMView(request):
	if request.method == 'POST':
		try:
			obj = growthFundingDM.objects.latest('id')
		except:
			obj = None
		objForm = growthFundingDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:growthFundingUrl')
	return HttpResponse('Invalid Entry')

def growthFundingContactDMView(request):
	if request.method == 'POST':
		try:
			obj = growthFundingContactDM.objects.latest('id')
		except:
			obj = None
		objForm = growthFundingContactDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:growthFundingContactUrl')
	return HttpResponse('Invalid Entry')

def earlyFundingDMView(request):
	if request.method == 'POST':
		try:
			obj = earlyFundingDM.objects.latest('id')
		except:
			obj = None
		objForm = earlyFundingDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:earlyFundingUrl')
	return HttpResponse('Invalid Entry')

def earlyFundingContactDMView(request):
	if request.method == 'POST':
		try:
			obj = earlyFundingContactDM.objects.latest('id')
		except:
			obj = None
		objForm = earlyFundingContactDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:earlyFundingContactUrl')
	return HttpResponse('Invalid Entry')

def seedFundingBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(seedFundingBanner, pk=pkID)
		objForm = seedFundingBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def seedFundRaisingJourneyView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(seedFundRaisingJourney, pk=pkID)
		objForm = seedFundRaisingJourneyForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def seedFundingAppFeatureView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(seedFundingAppFeature, pk=pkID)
		objForm = seedFundingAppFeatureForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def seedFundingFAQMainView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(seedFundingFAQMain, pk=pkID)
		objForm = seedFundingFAQMainForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def seedFundingFAQsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(seedFundingFAQs, pk=pkID)
		objForm = seedFundingFAQsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def seedFundingPricingPlanView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(seedFundingPricingPlan, pk=pkID)
		objForm = seedFundingPricingPlanForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def seedFundingPackagesView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(seedFundingPackages, pk=pkID)
		objForm = seedFundingPackagesForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')



def growthFundingBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(growthFundingBanner, pk=pkID)
		objForm = growthFundingBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def growthFundRaisingJourneyView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(growthFundRaisingJourney, pk=pkID)
		objForm = growthFundRaisingJourneyForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def growthFundingAppFeatureView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(growthFundingAppFeature, pk=pkID)
		objForm = growthFundingAppFeatureForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def growthFundingFAQMainView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(growthFundingFAQMain, pk=pkID)
		objForm = growthFundingFAQMainForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


def growthFundingFAQsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(growthFundingFAQs, pk=pkID)
		objForm = growthFundingFAQsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def growthFundingPricingPlanView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(growthFundingPricingPlan, pk=pkID)
		objForm = growthFundingPricingPlanForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def growthFundingPackagesView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(growthFundingPackages, pk=pkID)
		objForm = growthFundingPackagesForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def earlyFundingBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(earlyFundingBanner, pk=pkID)
		objForm = earlyFundingBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def earlyFundRaisingJourneyView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(earlyFundRaisingJourney, pk=pkID)
		objForm = earlyFundRaisingJourneyForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def earlyFundingAppFeatureView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(earlyFundingAppFeature, pk=pkID)
		objForm = earlyFundingAppFeatureForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def earlyFundingFAQMainView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(earlyFundingFAQMain, pk=pkID)
		objForm = earlyFundingFAQMainForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def earlyFundingFAQsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(earlyFundingFAQs, pk=pkID)
		objForm = earlyFundingFAQsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def earlyFundingPricingPlanView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(earlyFundingPricingPlan, pk=pkID)
		objForm = earlyFundingPricingPlanForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def earlyFundingPackagesView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(earlyFundingPackages, pk=pkID)
		objForm = earlyFundingPackagesForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def seedFundingView(request):

	try:
		seedFundingBannerInst = seedFundingBanner.objects.latest('id')

	except:
		seedFundingBannerInst = None
	seedFundingBannerInstForm = seedFundingBannerForm(instance=seedFundingBannerInst)

	try:
		seedFundRaisingJourneyInst = seedFundRaisingJourney.objects.latest('id')
		
	except:
		seedFundRaisingJourneyInst = None
	seedFundRaisingJourneyInstForm = seedFundRaisingJourneyForm(instance=seedFundRaisingJourneyInst)

	try:
		seedFundingFAQMainInst = seedFundingFAQMain.objects.latest('id')		

	except:
		seedFundingFAQMainInst = None	
	seedFundingFAQMainInstForm = seedFundingFAQMainForm(instance=seedFundingFAQMainInst)
	

	try:
		seedFundingAppFeatureInst = seedFundingAppFeature.objects.latest('id')

	except:
		seedFundingAppFeatureInst = None
	seedFundingAppFeatureInstForm = seedFundingAppFeatureForm(instance=seedFundingAppFeatureInst)

	try:
		seedFundingPricingPlanInst = seedFundingPricingPlan.objects.latest('id')

	except:
		seedFundingPricingPlanInst = None
	seedFundingPricingPlanInstForm =seedFundingPricingPlanForm(instance=seedFundingPricingPlanInst)

	try:
		seedFundingDMInst = seedFundingDM.objects.latest('id')
	except:
		seedFundingDMInst = None
	seedFundingDMInstForm =seedFundingDMForm(instance=seedFundingDMInst)


	seedFundingFAQsInst = seedFundingFAQs.objects.all().order_by('id')
	seedFundingFAQsInstForm = seedFundingFAQsForm()


	try:
		seedFundingPackagesInst = seedFundingPackages.objects.latest('id')
	except:
		seedFundingPackagesInst = None
	seedFundingPackagesInstForm =seedFundingPackagesForm(instance=seedFundingPackagesInst)


	context = {
	'seedFundingBannerInst':seedFundingBannerInst,
	'seedFundingBannerInstForm' : seedFundingBannerInstForm,

	'seedFundRaisingJourneyInst':seedFundRaisingJourneyInst,
	'seedFundRaisingJourneyInstForm' : seedFundRaisingJourneyInstForm,

	'seedFundingFAQMainInst':seedFundingFAQMainInst,
	'seedFundingFAQMainInstForm' : seedFundingFAQMainInstForm,

	'seedFundingPricingPlanInst':seedFundingPricingPlanInst,
	'seedFundingPricingPlanInstForm' :seedFundingPricingPlanInstForm,

	'seedFundingAppFeatureInst':seedFundingAppFeatureInst,
	'seedFundingAppFeatureInstForm' : seedFundingAppFeatureInstForm,

	'seedFundingFAQsInst':seedFundingFAQsInst,
	'seedFundingFAQsInstForm' : seedFundingFAQsInstForm,

	'seedFundingPackagesInst':seedFundingPackagesInst,
	'seedFundingPackagesInstForm' : seedFundingPackagesInstForm,

	'seedFundingDMInst':seedFundingDMInst,
	'seedFundingDMInstForm' : seedFundingDMInstForm,

	}
	return render(request,'productPages/UI/seedFunding.html', context)


def growthFundingView(request):

	try:
		growthFundingBannerInst = growthFundingBanner.objects.latest('id')
	except:
		growthFundingBannerInst = None
	growthFundingBannerInstForm = growthFundingBannerForm(instance=growthFundingBannerInst)


	try:
		growthFundRaisingJourneyInst = growthFundRaisingJourney.objects.latest('id')
	except:
		growthFundRaisingJourneyInst = None
	growthFundRaisingJourneyInstForm = growthFundRaisingJourneyForm(instance=growthFundRaisingJourneyInst)


	try:
		growthFundingFAQMainInst = growthFundingFAQMain.objects.latest('id')
	except:
		growthFundingFAQMainInst = None
	growthFundingFAQMainInstForm = growthFundingFAQMainForm(instance=growthFundingFAQMainInst)
	

	try:
		growthFundingPricingPlanInst = growthFundingPricingPlan.objects.latest('id')
	except:
		growthFundingPricingPlanInst = None
	growthFundingPricingPlanInstForm =growthFundingPricingPlanForm(instance=growthFundingPricingPlanInst)


	try:
		growthFundingAppFeatureInst = growthFundingAppFeature.objects.latest('id')
	except:
		growthFundingAppFeatureInst = None	
	growthFundingAppFeatureInstForm = growthFundingAppFeatureForm(instance=growthFundingAppFeatureInst)

	try:
		growthFundingDMInst = growthFundingDM.objects.latest('id')
	except:
		growthFundingDMInst = None
	growthFundingDMInstForm =growthFundingDMForm(instance=growthFundingDMInst)


	growthFundingFAQsInst = growthFundingFAQs.objects.all().order_by('id')
	growthFundingFAQsInstForm = growthFundingFAQsForm()

	

	try:
		growthFundingPackagesInst = growthFundingPackages.objects.latest('id')
	except:
		growthFundingPackagesInst = None
	growthFundingPackagesInstForm =growthFundingPackagesForm(instance=growthFundingPackagesInst)

	context = {
	'growthFundingBannerInst':growthFundingBannerInst,
	'growthFundingBannerInstForm' : growthFundingBannerInstForm,


	'growthFundRaisingJourneyInst':growthFundRaisingJourneyInst,
	'growthFundRaisingJourneyInstForm' : growthFundRaisingJourneyInstForm,

	'growthFundingFAQMainInst':growthFundingFAQMainInst,
	'growthFundingFAQMainInstForm' : growthFundingFAQMainInstForm,


	'growthFundingPricingPlanInst':growthFundingPricingPlanInst,
	'growthFundingPricingPlanInstForm' :growthFundingPricingPlanInstForm,

	'growthFundingAppFeatureInst':growthFundingAppFeatureInst,
	'growthFundingAppFeatureInstForm' : growthFundingAppFeatureInstForm,

	'growthFundingFAQsInst':growthFundingFAQsInst,
	'growthFundingFAQsInstForm' : growthFundingFAQsInstForm,

	'growthFundingPackagesInst':growthFundingPackagesInst,
	'growthFundingPackagesInstForm' : growthFundingPackagesInstForm,

	'growthFundingDMInst':growthFundingDMInst,
	'growthFundingDMInstForm' : growthFundingDMInstForm,

	# 'growthFundingContactUsSignupInst' : growthFundingContactUsSignupInst,
	# 'growthFundingContactUsSignupInstForm' : growthFundingContactUsSignupInstForm,


	}
	return render(request,'productPages/UI/growthFunding.html', context)


def earlyFundingView(request):

	try:
		earlyFundingBannerInst = earlyFundingBanner.objects.latest('id')
	except:
		earlyFundingBannerInst = None
	earlyFundingBannerInstForm = earlyFundingBannerForm(instance=earlyFundingBannerInst)


	try:
		earlyFundRaisingJourneyInst = earlyFundRaisingJourney.objects.latest('id')
	except:
		earlyFundRaisingJourneyInst = None
	earlyFundRaisingJourneyInstForm = earlyFundRaisingJourneyForm(instance=earlyFundRaisingJourneyInst)


	try:
		earlyFundingFAQMainInst = earlyFundingFAQMain.objects.latest('id')
	except:
		earlyFundingFAQMainInst = None
	earlyFundingFAQMainInstForm = earlyFundingFAQMainForm(instance=earlyFundingFAQMainInst)


	try:
		earlyFundingPricingPlanInst = earlyFundingPricingPlan.objects.latest('id')
	except:
		earlyFundingPricingPlanInst = None
	earlyFundingPricingPlanInstForm =earlyFundingPricingPlanForm(instance=earlyFundingPricingPlanInst)


	try:
		earlyFundingAppFeatureInst = earlyFundingAppFeature.objects.latest('id')
	except:
		earlyFundingAppFeatureInst = None
	earlyFundingAppFeatureInstForm =earlyFundingAppFeatureForm(instance=earlyFundingAppFeatureInst)

	try:
		earlyFundingDMInst = earlyFundingDM.objects.latest('id')
	except:
		earlyFundingDMInst = None
	

	earlyFundingFAQsInst = earlyFundingFAQs.objects.all().order_by('id')
	earlyFundingFAQsInstForm = earlyFundingFAQsForm()

	try:
		earlyFundingPackagesInst = earlyFundingPackages.objects.latest('id')
	except:
		earlyFundingPackagesInst = None
	earlyFundingPackagesInstForm =earlyFundingPackagesForm(instance=earlyFundingPackagesInst)
	
	context = {
	'earlyFundingBannerInst':earlyFundingBannerInst,
	'earlyFundingBannerInstForm' : earlyFundingBannerInstForm,


	'earlyFundRaisingJourneyInst':earlyFundRaisingJourneyInst,
	'earlyFundRaisingJourneyInstForm' : earlyFundRaisingJourneyInstForm,

	'earlyFundingFAQMainInst':earlyFundingFAQMainInst,
	'earlyFundingFAQMainInstForm' : earlyFundingFAQMainInstForm,

	'earlyFundingPricingPlanInst':earlyFundingPricingPlanInst,
	'earlyFundingPricingPlanInstForm' :earlyFundingPricingPlanInstForm,

	'earlyFundingAppFeatureInst':earlyFundingAppFeatureInst,
	'earlyFundingAppFeatureInstForm' : earlyFundingAppFeatureInstForm,

	'earlyFundingFAQsInst':earlyFundingFAQsInst,
	'earlyFundingFAQsInstForm' : earlyFundingFAQsInstForm,

	'earlyFundingPackagesInst':earlyFundingPackagesInst,
	'earlyFundingPackagesInstForm' : earlyFundingPackagesInstForm,

	'earlyFundingDMInst':earlyFundingDMInst,
	
	}
	return render(request,'productPages/UI/earlyFunding.html', context)


def seedFundingContactUsBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(seedFundingContactUsBanner, pk=pkID)
		objForm = seedFundingContactUsBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def growthFundingContactUsBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(growthFundingContactUsBanner, pk=pkID)
		objForm = growthFundingContactUsBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def earlyFundingContactUsBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(earlyFundingContactUsBanner, pk=pkID)
		objForm = earlyFundingContactUsBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def growthFundingContactUsKnowMoreView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(growthFundingContactUsKnowMore, pk=pkID)
		objForm = growthFundingContactUsKnowMoreForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def earlyFundingContactUsKnowMoreView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(earlyFundingContactUsKnowMore, pk=pkID)
		objForm = earlyFundingContactUsKnowMoreForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def seedFundingContactUsKnowMoreView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(seedFundingContactUsKnowMore, pk=pkID)
		objForm = seedFundingContactUsKnowMoreForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def seedFundingContactUsKnowMoreFAQsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(seedFundingContactUsKnowMoreFAQs, pk=pkID)
		objForm = seedFundingContactUsKnowMoreFAQsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def growthFundingContactUsKnowMoreFAQsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(growthFundingContactUsKnowMoreFAQs, pk=pkID)
		objForm = growthFundingContactUsKnowMoreFAQsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def earlyFundingContactUsKnowMoreFAQsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(earlyFundingContactUsKnowMoreFAQs, pk=pkID)
		objForm = earlyFundingContactUsKnowMoreFAQsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def growthFundingContactView(request):
	if request.method == 'POST':
		objForm = growthFundingContactUsSignupForm(request.POST)
		redirectTo = request.POST.get('redirectTo')
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			# messages.success(request, 'Data sent for verification')
			redirectTo += '?success=true'
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def seedFundingContactView(request):
	if request.method == 'POST':
		objForm = seedFundingContactUsSignupForm(request.POST)
		redirectTo = request.POST.get('redirectTo')
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			# messages.success(request, 'Data sent for verification')
			redirectTo += '?success=true'
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def earlyFundingContactView(request):
	if request.method == 'POST':
		objForm = earlyFundingContactUsSignupForm(request.POST)
		redirectTo = request.POST.get('redirectTo')
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			# messages.success(request, 'Data sent for verification')
			redirectTo += '?success=true'
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')
	

#render View
def earlyFundingContactSignupView(request):

	try:
		earlyFundingContactUsBannerInst = earlyFundingContactUsBanner.objects.latest('id')

	except:
		earlyFundingContactUsBannerInst = None
	earlyFundingContactUsBannerInstForm = earlyFundingContactUsBannerForm(instance=earlyFundingContactUsBannerInst)

	try:
		earlyFundingContactUsKnowMoreInst = earlyFundingContactUsKnowMore.objects.latest('id')

	except:
		earlyFundingContactUsKnowMoreInst = None
	earlyFundingContactUsKnowMoreInstForm = earlyFundingContactUsKnowMoreForm(instance=earlyFundingContactUsKnowMoreInst)

	try:
		earlyFundingContactDMInst = earlyFundingContactDM.objects.latest('id')

	except:
		earlyFundingContactDMInst = None


	earlyFundingContactUsKnowMoreFAQsInst = earlyFundingContactUsKnowMoreFAQs.objects.all().order_by('id')
	earlyFundingContactUsKnowMoreFAQsInstForm = earlyFundingContactUsKnowMoreFAQsForm()

	objForm = earlyFundingContactUsSignupForm()
	countryList = country.objects.all()
	context = {
		'earlyFundingContactUsBannerInst' : earlyFundingContactUsBannerInst,
		'earlyFundingContactUsBannerInstForm' : earlyFundingContactUsBannerInstForm,

		'earlyFundingContactUsKnowMoreInst' : earlyFundingContactUsKnowMoreInst,
		'earlyFundingContactUsKnowMoreInstForm' : earlyFundingContactUsKnowMoreInstForm,

		'earlyFundingContactUsKnowMoreFAQsInst' : earlyFundingContactUsKnowMoreFAQsInst,
		'earlyFundingContactUsKnowMoreFAQsInstForm' : earlyFundingContactUsKnowMoreFAQsInstForm,

		'earlyFundingContactDMInst':earlyFundingContactDMInst,
		'objForm':objForm,
		'countryList':countryList,
	}
	return render(request, 'productPages/UI/earlyFundingContact.html', context)

def growthFundingContactSignupView(request):

	try:
		growthFundingContactUsBannerInst = growthFundingContactUsBanner.objects.latest('id')

	except:
		growthFundingContactUsBannerInst = None
	growthFundingContactUsBannerInstForm = growthFundingContactUsBannerForm(instance=growthFundingContactUsBannerInst)

	try:
		growthFundingContactUsKnowMoreInst = growthFundingContactUsKnowMore.objects.latest('id')

	except:
		growthFundingContactUsKnowMoreInst = None
	growthFundingContactUsKnowMoreInstForm = growthFundingContactUsKnowMoreForm(instance=growthFundingContactUsKnowMoreInst)

	try:
		growthFundingContactDMInst = growthFundingContactDM.objects.latest('id')

	except:
		growthFundingContactDMInst = None


	growthFundingContactUsKnowMoreFAQsInst = growthFundingContactUsKnowMoreFAQs.objects.all().order_by('id')
	growthFundingContactUsKnowMoreFAQsInstForm = growthFundingContactUsKnowMoreFAQsForm()

	objForm = growthFundingContactUsSignupForm()
	countryList = country.objects.all()

	context = {
		'growthFundingContactUsBannerInst' : growthFundingContactUsBannerInst,
		'growthFundingContactUsBannerInstForm' : growthFundingContactUsBannerInstForm,

		'growthFundingContactUsKnowMoreInst':growthFundingContactUsKnowMoreInst,
		'growthFundingContactUsKnowMoreInstForm':growthFundingContactUsKnowMoreInstForm,

		'growthFundingContactUsKnowMoreFAQsInst' : growthFundingContactUsKnowMoreFAQsInst,
		'growthFundingContactUsKnowMoreFAQsInstForm' : growthFundingContactUsKnowMoreFAQsInstForm,

		'growthFundingContactDMInst':growthFundingContactDMInst,
		'objForm':objForm,
		'countryList':countryList,
	}
	return render(request, 'productPages/UI/growthFundingContact.html', context)

def seedFundingContactSignupView(request):

	try:
		seedFundingContactUsBannerInst = seedFundingContactUsBanner.objects.latest('id')

	except:
		seedFundingContactUsBannerInst = None
	seedFundingContactUsBannerInstForm = seedFundingContactUsBannerForm(instance=seedFundingContactUsBannerInst)

	try:
		seedFundingContactUsKnowMoreInst = seedFundingContactUsKnowMore.objects.latest('id')

	except:
		seedFundingContactUsKnowMoreInst = None
	seedFundingContactUsKnowMoreInstForm = seedFundingContactUsKnowMoreForm(instance=seedFundingContactUsKnowMoreInst)

	try:
		seedFundingContactDMInst = seedFundingContactDM.objects.latest('id')

	except:
		seedFundingContactDMInst = None

	seedFundingContactUsKnowMoreFAQsInst = seedFundingContactUsKnowMoreFAQs.objects.all().order_by('id')
	seedFundingContactUsKnowMoreFAQsInstForm = seedFundingContactUsKnowMoreFAQsForm()
	objForm = seedFundingContactUsSignupForm()
	# cityList = city.objects.all()
	countryList = country.objects.all()

	context = {
		'seedFundingContactUsBannerInst' : seedFundingContactUsBannerInst,
		'seedFundingContactUsBannerInstForm' : seedFundingContactUsBannerInstForm,

		'seedFundingContactUsKnowMoreInst' : seedFundingContactUsKnowMoreInst,
		'seedFundingContactUsKnowMoreInstForm' : seedFundingContactUsKnowMoreInstForm,

		'seedFundingContactUsKnowMoreFAQsInst' : seedFundingContactUsKnowMoreFAQsInst,
		'seedFundingContactUsKnowMoreFAQsInstForm' : seedFundingContactUsKnowMoreFAQsInstForm,
		
		'seedFundingContactDMInst':seedFundingContactDMInst,
		'objForm':objForm,
		'countryList':countryList,

	}
	return render(request, 'productPages/UI/seedFundingContact.html', context)

#



def sellESOPDMView(request):
	if request.method == 'POST':
		try:
			obj = sellESOPDM.objects.latest('id')
		except:
			obj = None
		objForm = sellESOPDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:sellESOPUrl')
	return HttpResponse('Invalid Entry')

def sellESOPContactDMView(request):
	if request.method == 'POST':
		try:
			obj = sellESOPContactDM.objects.latest('id')
		except:
			obj = None
		objForm = sellESOPContactDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:sellESOPContactUrl')
	return HttpResponse('Invalid Entry')
	


def sellESOPBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPBanner, pk=pkID)
		objForm = sellESOPBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)


def sellESOPAboutUsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPAboutUs, pk=pkID)
		objForm = sellESOPAboutUsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)

def sellESOPFineWordsAboutUsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPFineWordsAboutUs, pk=pkID)
		objForm = sellESOPFineWordsAboutUsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)

def sellESOPVideoView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPVideo, pk=pkID)
		objForm = sellESOPVideoForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)

def sellESOPJourneyView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPJourney, pk=pkID)
		objForm = sellESOPJourneyForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)

#
def sellESOPAppFeaturesView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPAppFeatures, pk=pkID)
		objForm = sellESOPAppFeaturesForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)

def sellESOPCardsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPCards, pk=pkID)
		objForm = sellESOPCardsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)

def sellESOPRunningNumbersView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPRunningNumbers, pk=pkID)
		objForm = sellESOPRunningNumbersForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)

def sellESOPFAQMainView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPFAQMain, pk=pkID)
		objForm = sellESOPFAQMainForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)

def sellESOPFAQsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPFAQs, pk=pkID)
		objForm = sellESOPFAQsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)



def sellESOPView(request):
	
	try:
		sellESOPBannerInst = sellESOPBanner.objects.latest('id')
	except:
		sellESOPBannerInst = None
	sellESOPBannerInstForm = sellESOPBannerForm(instance=sellESOPBannerInst)


	try:
		sellESOPAboutUsInst = sellESOPAboutUs.objects.latest('id')
	except:
		sellESOPAboutUsInst = None
	sellESOPAboutUsInstForm = sellESOPAboutUsForm(instance=sellESOPAboutUsInst)
	

	try:
		sellESOPFineWordsAboutUsInst = sellESOPFineWordsAboutUs.objects.latest('id')
	except:
		sellESOPFineWordsAboutUsInst = None
	sellESOPFineWordsAboutUsInstForm = sellESOPFineWordsAboutUsForm(instance=sellESOPFineWordsAboutUsInst)
	

	try:
		sellESOPVideoInst = sellESOPVideo.objects.latest('id')
	except:
		sellESOPVideoInst = None
	sellESOPVideoInstForm = sellESOPVideoForm(instance=sellESOPVideoInst)
	

	try:
		sellESOPJourneyInst = sellESOPJourney.objects.latest('id')
	except:
		sellESOPJourneyInst = None
	sellESOPJourneyInstForm = sellESOPJourneyForm(instance=sellESOPJourneyInst)
	

	try:
		sellESOPFAQMainInst = sellESOPFAQMain.objects.latest('id')
	except:
		sellESOPFAQMainInst = None
	sellESOPFAQMainInstForm = sellESOPFAQMainForm(instance=sellESOPFAQMainInst)


	try:
		sellESOPAppFeaturesInst = sellESOPAppFeatures.objects.latest('id')
	except:
		sellESOPAppFeaturesInst = None
	sellESOPAppFeaturesInstForm = sellESOPAppFeaturesForm(instance=sellESOPAppFeaturesInst)

	try:
		sellESOPDMInst = sellESOPDM.objects.latest('id')
	except:
		sellESOPDMInst = None


	sellESOPCardsInst = sellESOPCards.objects.all().order_by('id')
	sellESOPCardsInstForm = sellESOPCardsForm()

	sellESOPFAQsInst = sellESOPFAQs.objects.all().order_by('id')
	sellESOPFAQsInstForm = sellESOPFAQsForm()

	sellESOPRunningNumbersInst = sellESOPRunningNumbers.objects.all().order_by('id')
	sellESOPRunningNumbersInstForm = sellESOPRunningNumbersForm()



	context = {
		'sellESOPBannerInst' : sellESOPBannerInst,
		'sellESOPBannerInstForm' : sellESOPBannerInstForm,

		'sellESOPAboutUsInst' : sellESOPAboutUsInst,
		'sellESOPAboutUsInstForm' : sellESOPAboutUsInstForm,

		'sellESOPFineWordsAboutUsInst' : sellESOPFineWordsAboutUsInst,
		'sellESOPFineWordsAboutUsInstForm' : sellESOPFineWordsAboutUsInstForm,

		'sellESOPFAQMainInst' : sellESOPFAQMainInst,
		'sellESOPFAQMainInstForm' : sellESOPFAQMainInstForm,

		'sellESOPJourneyInst' : sellESOPJourneyInst,
		'sellESOPJourneyInstForm' : sellESOPJourneyInstForm,

		'sellESOPVideoInst' : sellESOPVideoInst,
		'sellESOPVideoInstForm' : sellESOPVideoInstForm,

		'sellESOPRunningNumbersInst' : sellESOPRunningNumbersInst,
		'sellESOPRunningNumbersInstForm' : sellESOPRunningNumbersInstForm,

		'sellESOPAppFeaturesInst' : sellESOPAppFeaturesInst,
		'sellESOPAppFeaturesInstForm' : sellESOPAppFeaturesInstForm,

		'sellESOPCardsInst' : sellESOPCardsInst,
		'sellESOPCardsInstForm' : sellESOPCardsInstForm,

		'sellESOPFAQsInst' : sellESOPFAQsInst,
		'sellESOPFAQsInstForm' : sellESOPFAQsInstForm,

		'sellESOPDMInst' : sellESOPDMInst,

	}

	return render(request, 'productPages/UI/sellESOP.html', context)



#
def sellESOPContactView(request):
	if request.method == 'POST':
		objForm = sellESOPContactUsForm(request.POST)
		redirectTo = request.POST.get('redirectTo')
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			# messages.success(request, 'Data sent for verification')
			redirectTo += '?success=true'
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')



def sellESOPContactUsBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPContactUsBanner, pk=pkID)
		objForm = sellESOPContactUsBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellESOPContactUsKnowMoreView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPContactUsKnowMore, pk=pkID)
		objForm = sellESOPContactUsKnowMoreForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellESOPContactUsKnowMoreFAQsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellESOPContactUsKnowMoreFAQs, pk=pkID)
		objForm = sellESOPContactUsKnowMoreFAQsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellESOPContactSignupView(request):

	try:
		sellESOPContactUsBannerInst = sellESOPContactUsBanner.objects.latest('id')

	except:
		sellESOPContactUsBannerInst = None
	sellESOPContactUsBannerInstForm = sellESOPContactUsBannerForm(instance=sellESOPContactUsBannerInst)

	try:
		sellESOPContactUsKnowMoreInst = sellESOPContactUsKnowMore.objects.latest('id')

	except:
		sellESOPContactUsKnowMoreInst = None
	sellESOPContactUsKnowMoreInstForm = sellESOPContactUsKnowMoreForm(instance=sellESOPContactUsKnowMoreInst)

	try:
		sellESOPContactDMInst = sellESOPContactDM.objects.latest('id')

	except:
		sellESOPContactDMInst = None


	sellESOPContactUsKnowMoreFAQsInst = sellESOPContactUsKnowMoreFAQs.objects.all().order_by('id')
	sellESOPContactUsKnowMoreFAQsInstForm = sellESOPContactUsKnowMoreFAQsForm()

	objForm = sellESOPContactUsForm()
	countryList = country.objects.all()

	context = {
		'sellESOPContactUsBannerInst' : sellESOPContactUsBannerInst,
		'sellESOPContactUsBannerInstForm' : sellESOPContactUsBannerInstForm,

		'sellESOPContactUsKnowMoreInst' : sellESOPContactUsKnowMoreInst,
		'sellESOPContactUsKnowMoreInstForm' : sellESOPContactUsKnowMoreInstForm,

		'sellESOPContactUsKnowMoreFAQsInst' : sellESOPContactUsKnowMoreFAQsInst,
		'sellESOPContactUsKnowMoreFAQsInstForm' : sellESOPContactUsKnowMoreFAQsInstForm,

		'sellESOPContactDMInst':sellESOPContactDMInst,
		'countryList':countryList,
		'objForm':objForm,

	}
	return render(request, 'productPages/UI/sellESOPContact.html', context)

# private-boutique



def privateBoutiqueFAQNRIView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueFAQNRI, pk=pkID)
		objForm = privateBoutiqueFAQNRIForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


def privateBoutiqueFAQLegalityView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueFAQLegality, pk=pkID)
		objForm = privateBoutiqueFAQLegalityForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')



def privateBoutiqueSuccessStoriesView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueSuccessStories, pk=pkID)
		objForm = privateBoutiqueSuccessStoriesForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')





def privateBoutiqueCategoryView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueCategory, pk=pkID)
		objForm = privateBoutiqueCategoryForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


def privateBoutiqueBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueBanner, pk=pkID)
		objForm = privateBoutiqueBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')



def privateBoutiqueRunningCardsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueRunningCards, pk=pkID)
		objForm = privateBoutiqueRunningCardsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')



def privateBoutiqueInvestingProcessImageView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueInvestingProcessImage, pk=pkID)
		objForm = privateBoutiqueInvestingProcessImageForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


def privateBoutiqueInvestingProcessCardsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueInvestingProcessCards, pk=pkID)
		objForm = privateBoutiqueInvestingProcessCardsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def privateBoutiqueSellingProcessCardsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueSellingProcessCards, pk=pkID)
		objForm = privateBoutiqueSellingProcessCardsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def privateBoutiqueSellingProcessImageView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueSellingProcessImage, pk=pkID)
		objForm = privateBoutiqueSellingProcessImageForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def privateBoutiqueWhyToInvestCardsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueWhyToInvestCards, pk=pkID)
		objForm = privateBoutiqueWhyToInvestCardsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


def privateBoutiqueWhyToInvestContentView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueWhyToInvestContent, pk=pkID)
		objForm = privateBoutiqueWhyToInvestContentForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')




def privateBoutiqueFAQInvestmentView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueFAQInvestment, pk=pkID)
		objForm = privateBoutiqueFAQInvestmentForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


def privateBoutiqueFAQTaxImplicationsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueFAQTaxImplications, pk=pkID)
		objForm = privateBoutiqueFAQTaxImplicationsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


def privateBoutiqueDMView(request):
	if request.method == 'POST':
		try:
			obj = privateBoutiqueDM.objects.latest('id')
		except:
			obj = None
		objForm = privateBoutiqueDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:privateBoutiqueUrl')
	return HttpResponse('Invalid Entry')



def privateBoutiqueContactUsBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueContactUsBanner, pk=pkID)
		objForm = privateBoutiqueContactUsBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def privateBoutiqueContactUsKnowMoreView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueContactUsKnowMore, pk=pkID)
		objForm = privateBoutiqueContactUsKnowMoreForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def privateBoutiqueContactUsKnowMoreFAQsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(privateBoutiqueContactUsKnowMoreFAQs, pk=pkID)
		objForm = privateBoutiqueContactUsKnowMoreFAQsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def privateBoutiqueContactUsView(request):
	if request.method == 'POST':
		objForm = privateBoutiqueContactUsForm(request.POST)
		redirectTo = request.POST.get('redirectTo')
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			# messages.success(request, 'Data sent for verification')
			redirectTo += '?success=true'
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def privateBoutiqueContactDMView(request):
	if request.method == 'POST':
		try:
			obj = privateBoutiqueContactDM.objects.latest('id')
		except:
			obj = None
		objForm = privateBoutiqueContactDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:privateBoutiqueContactUsSignupUrl')
	return HttpResponse('Invalid Entry')


def absoluteReturnFormula(investmentPrice, presentPrice):
	absoluteVal = 0 
	if investmentPrice and presentPrice:
		absoluteVal = ((presentPrice - investmentPrice)/(investmentPrice))*100
	return absoluteVal


def privateBoutiqueView(request):
	# stock = get_object_or_404(stockBasicDetail)
	# currentPrice = localOrScreenerPriceView()

	try:
		privateBoutiqueBannerInst = privateBoutiqueBanner.objects.latest('id')
	except:
		privateBoutiqueBannerInst = None
	privateBoutiqueBannerInstForm = privateBoutiqueBannerForm(instance=privateBoutiqueBannerInst)
	
	try:
		privateBoutiqueInvestingProcessImageInst = privateBoutiqueInvestingProcessImage.objects.latest('id')
	except:
		privateBoutiqueInvestingProcessImageInst = None
	privateBoutiqueInvestingProcessImageInstForm = privateBoutiqueInvestingProcessImageForm(instance=privateBoutiqueInvestingProcessImageInst)

	try:
		privateBoutiqueSellingProcessImageInst = privateBoutiqueSellingProcessImage.objects.latest('id')
	except:
		privateBoutiqueSellingProcessImageInst = None
	privateBoutiqueSellingProcessImageInstForm = privateBoutiqueSellingProcessImageForm(instance=privateBoutiqueSellingProcessImageInst)

	try:
		privateBoutiqueWhyToInvestContentInst = privateBoutiqueWhyToInvestContent.objects.latest('id')
	except:
		privateBoutiqueWhyToInvestContentInst = None
	privateBoutiqueWhyToInvestContentInstForm = privateBoutiqueWhyToInvestContentForm(instance=privateBoutiqueWhyToInvestContentInst)


	# try:
	# 	privateBoutiqueSuccessStoriesInst = privateBoutiqueSuccessStories.objects.latest('id')
	# except:
	# 	privateBoutiqueSuccessStoriesInst = None
	# privateBoutiqueSuccessStoriesInstForm = privateBoutiqueSuccessStoriesForm(instance=privateBoutiqueSuccessStoriesInst)


	


	try:
		privateBoutiqueDMInst = privateBoutiqueDM.objects.latest('id')
	except:
		privateBoutiqueDMInst = None
	privateBoutiqueDMInstForm = privateBoutiqueDMForm(instance=privateBoutiqueDMInst)


	privateBoutiqueSuccessStoriesInsts = privateBoutiqueSuccessStories.objects.all().order_by('stockName__stockName')
	successStoriesDict = {}
	for item in privateBoutiqueSuccessStoriesInsts:
		absoluteReturn = absoluteReturnFormula(item.investmentPrice, item.get_current_price())		
		successStoriesDict[item] = absoluteReturn
	
	privateBoutiqueSuccessStoriesInstForm = privateBoutiqueSuccessStoriesForm()

	# absoluteReturn = absoluteReturnFormula(privateBoutiqueSuccessStoriesInst.investmentPrice, privateBoutiqueSuccessStoriesInst.presentPrice)

	# if privateBoutiqueSuccessStoriesInst:
	# 	currentPrice = privateBoutiqueSuccessStoriesInst.get_current_price()

	privateBoutiqueRunningCardsInst = privateBoutiqueRunningCards.objects.all().order_by('id')
	privateBoutiqueRunningCardsInstForm = privateBoutiqueRunningCardsForm()

	privateBoutiqueInvestingProcessCardsInst = privateBoutiqueInvestingProcessCards.objects.all().order_by('id')
	privateBoutiqueInvestingProcessCardsInstForm = privateBoutiqueInvestingProcessCardsForm()

	privateBoutiqueSellingProcessCardsInst = privateBoutiqueSellingProcessCards.objects.all().order_by('id')
	privateBoutiqueSellingProcessCardsInstForm = privateBoutiqueSellingProcessCardsForm()

	privateBoutiqueWhyToInvestCardsInst = privateBoutiqueWhyToInvestCards.objects.all().order_by('id')
	privateBoutiqueWhyToInvestCardsInstForm = privateBoutiqueWhyToInvestCardsForm()

	privateBoutiqueFAQInvestmentInst = privateBoutiqueFAQInvestment.objects.all().order_by('id')
	privateBoutiqueFAQInvestmentInstForm = privateBoutiqueFAQInvestmentForm()

	privateBoutiqueFAQTaxImplicationsInst = privateBoutiqueFAQTaxImplications.objects.all().order_by('id')
	privateBoutiqueFAQTaxImplicationsInstForm = privateBoutiqueFAQTaxImplicationsForm()

	privateBoutiqueFAQLegalityInst = privateBoutiqueFAQLegality.objects.all().order_by('id')
	privateBoutiqueFAQLegalityInstForm = privateBoutiqueFAQLegalityForm()

	privateBoutiqueFAQNRIInst = privateBoutiqueFAQNRI.objects.all().order_by('id')
	privateBoutiqueFAQNRIInstForm = privateBoutiqueFAQNRIForm()


	# categoryInst = categories.objects.all()

	stockBasicDetailInst = stockBasicDetail.objects.all().order_by('id')
	stockEssentialsInst = stockEssentials.objects.all().order_by('id')

	privateBoutiqueCategoryInst = privateBoutiqueCategory.objects.all().order_by('id')
	privateBoutiqueCategoryInstForm = privateBoutiqueCategoryForm()


	categoriesPairs = {};

	for item in privateBoutiqueCategoryInst:
		stockByCat = stockEssentials.objects.filter(category=item.category)
		categoriesPairs[item] = stockByCat
		# categoriesPairs.update({: item.stockBasicDetails})

	context = {
		# 'currentPrice':currentPrice,
		'privateBoutiqueFAQLegalityInst' : privateBoutiqueFAQLegalityInst,
		'privateBoutiqueFAQLegalityInstForm' : privateBoutiqueFAQLegalityInstForm,

		'privateBoutiqueFAQNRIInst' : privateBoutiqueFAQNRIInst,
		'privateBoutiqueFAQNRIInstForm' : privateBoutiqueFAQNRIInstForm,

		'privateBoutiqueBannerInst': privateBoutiqueBannerInst,
		'privateBoutiqueBannerInstForm' : privateBoutiqueBannerInstForm,

		'privateBoutiqueInvestingProcessImageInst' : privateBoutiqueInvestingProcessImageInst,
		'privateBoutiqueInvestingProcessImageInstForm' : privateBoutiqueInvestingProcessImageInstForm,

		'privateBoutiqueSellingProcessImageInst' : privateBoutiqueSellingProcessImageInst,
		'privateBoutiqueSellingProcessImageInstForm' : privateBoutiqueSellingProcessImageInstForm,

		'privateBoutiqueWhyToInvestContentInst' : privateBoutiqueWhyToInvestContentInst,
		'privateBoutiqueWhyToInvestContentInstForm' : privateBoutiqueWhyToInvestContentInstForm,

		'privateBoutiqueRunningCardsInst' : privateBoutiqueRunningCardsInst,
		'privateBoutiqueRunningCardsInstForm' : privateBoutiqueRunningCardsInstForm,

		'privateBoutiqueInvestingProcessCardsInst' : privateBoutiqueInvestingProcessCardsInst,
		'privateBoutiqueInvestingProcessCardsInstForm' : privateBoutiqueInvestingProcessCardsInstForm,

		'privateBoutiqueSellingProcessCardsInst' : privateBoutiqueSellingProcessCardsInst,
		'privateBoutiqueSellingProcessCardsInstForm' : privateBoutiqueSellingProcessCardsInstForm,

		'privateBoutiqueWhyToInvestCardsInst' : privateBoutiqueWhyToInvestCardsInst,
		'privateBoutiqueWhyToInvestCardsInstForm' : privateBoutiqueWhyToInvestCardsInstForm,

		'privateBoutiqueFAQInvestmentInst' : privateBoutiqueFAQInvestmentInst,
		'privateBoutiqueFAQInvestmentInstForm' : privateBoutiqueFAQInvestmentInstForm,

		'privateBoutiqueFAQTaxImplicationsInst' : privateBoutiqueFAQTaxImplicationsInst,
		'privateBoutiqueFAQTaxImplicationsInstForm' : privateBoutiqueFAQTaxImplicationsInstForm,

		'privateBoutiqueDMInst' : privateBoutiqueDMInst,
		'privateBoutiqueDMInstForm' : privateBoutiqueDMInst,

		'stockBasicDetailInst' : stockBasicDetailInst,
		'stockEssentialsInst' : stockEssentialsInst,

		'categoriesPairs' : categoriesPairs,
		'privateBoutiqueCategoryInst' : privateBoutiqueCategoryInst,
		'privateBoutiqueCategoryInstForm' : privateBoutiqueCategoryInstForm,

		'successStoriesDict': successStoriesDict,
		'privateBoutiqueSuccessStoriesInstForm':privateBoutiqueSuccessStoriesInstForm,


	}
	return render(request, 'productPages/UI/privateBoutique.html', context)


def privateBoutiqueContactUsSignupView(request):

	try:
		privateBoutiqueContactUsBannerInst = privateBoutiqueContactUsBanner.objects.latest('id')

	except:
		privateBoutiqueContactUsBannerInst = None
	privateBoutiqueContactUsBannerInstForm = privateBoutiqueContactUsBannerForm(instance=privateBoutiqueContactUsBannerInst)

	try:
		privateBoutiqueContactUsKnowMoreInst = privateBoutiqueContactUsKnowMore.objects.latest('id')

	except:
		privateBoutiqueContactUsKnowMoreInst = None
	privateBoutiqueContactUsKnowMoreInstForm = privateBoutiqueContactUsKnowMoreForm(instance=privateBoutiqueContactUsKnowMoreInst)

	try:
		privateBoutiqueContactDMInst = privateBoutiqueContactDM.objects.latest('id')

	except:
		privateBoutiqueContactDMInst = None


	privateBoutiqueContactUsKnowMoreFAQsInst = privateBoutiqueContactUsKnowMoreFAQs.objects.all().order_by('id')
	privateBoutiqueContactUsKnowMoreFAQsInstForm = privateBoutiqueContactUsKnowMoreFAQsForm()

	countryList = country.objects.all()
	

	objForm = privateBoutiqueContactUsForm()

	context = {
		'privateBoutiqueContactUsBannerInst' : privateBoutiqueContactUsBannerInst,
		'privateBoutiqueContactUsBannerInstForm' : privateBoutiqueContactUsBannerInstForm,
		'privateBoutiqueContactUsKnowMoreInst' : privateBoutiqueContactUsKnowMoreInst,
		'privateBoutiqueContactUsKnowMoreInstForm' : privateBoutiqueContactUsKnowMoreInstForm,
		'privateBoutiqueContactUsKnowMoreFAQsInst' : privateBoutiqueContactUsKnowMoreFAQsInst,
		'privateBoutiqueContactUsKnowMoreFAQsInstForm' : privateBoutiqueContactUsKnowMoreFAQsInstForm,
		'privateBoutiqueContactDMInst':privateBoutiqueContactDMInst,
		'countryList' : countryList,
		'objForm':objForm,

	}
	return render(request, 'productPages/UI/privateBoutiqueContact.html', context)

#
def sellYourStartupBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellYourStartupBanner, pk=pkID)
		objForm = sellYourStartupBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellYourStartupExposureView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellYourStartupExposure, pk=pkID)
		objForm = sellYourStartupExposureForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellYourStartupUnparalleledExposureView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellYourStartupUnparalleledExposure, pk=pkID)
		objForm = sellYourStartupUnparalleledExposureForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellYourStartupBusinessListView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellYourStartupBusinessList, pk=pkID)
		objForm = sellYourStartupBusinessListForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellYourStartupBusinessWorthView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellYourStartupBusinessWorth, pk=pkID)
		objForm = sellYourStartupBusinessWorthForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellYourStartupFAQMainView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellYourStartupFAQMain, pk=pkID)
		objForm = sellYourStartupFAQMainForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellYourStartupFAQsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellYourStartupFAQs, pk=pkID)
		objForm = sellYourStartupFAQsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellYourStartupDMView(request):
	if request.method == 'POST':
		try:
			obj = sellYourStartupDM.objects.latest('id')
		except:
			obj = None
		objForm = sellYourStartupDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:sellYourStartupUrl')
	return HttpResponse('Invalid Entry')

def sellYourStartupView(request):

	try:
		sellYourStartupBannerInst = sellYourStartupBanner.objects.latest('id')
	except:
		sellYourStartupBannerInst = None
	sellYourStartupBannerInstForm = sellYourStartupBannerForm(instance=sellYourStartupBannerInst)	

	try:
		sellYourStartupUnparalleledExposureInst = sellYourStartupUnparalleledExposure.objects.latest('id')
	except:
		sellYourStartupUnparalleledExposureInst = None
	sellYourStartupUnparalleledExposureInstForm = sellYourStartupUnparalleledExposureForm(instance=sellYourStartupUnparalleledExposureInst)
	
	try:
		sellYourStartupBusinessListInst = sellYourStartupBusinessList.objects.latest('id')
	except:
		sellYourStartupBusinessListInst = None
	sellYourStartupBusinessListInstForm = sellYourStartupBusinessListForm(instance=sellYourStartupBusinessListInst)
	
	try:
		sellYourStartupBusinessWorthInst = sellYourStartupBusinessWorth.objects.latest('id')
	except:
		sellYourStartupBusinessWorthInst = None
	sellYourStartupBusinessWorthInstForm = sellYourStartupBusinessWorthForm(instance=sellYourStartupBusinessWorthInst)	

	try:
		sellYourStartupFAQMainInst = sellYourStartupFAQMain.objects.latest('id')
	except:
		sellYourStartupFAQMainInst = None
	sellYourStartupFAQMainInstForm = sellYourStartupFAQMainForm(instance=sellYourStartupFAQMainInst)

	try:
		sellYourStartupDMInst = sellYourStartupDM.objects.latest('id')
	except:
		sellYourStartupDMInst = None
	sellYourStartupDMInstForm =sellYourStartupDMForm(instance=sellYourStartupDMInst)

	sellYourStartupExposureInst = sellYourStartupExposure.objects.all().order_by('id')
	sellYourStartupExposureInstForm = sellYourStartupExposureForm()

	sellYourStartupFAQsInst = sellYourStartupFAQs.objects.all().order_by('id')
	sellYourStartupFAQsInstForm = sellYourStartupFAQsForm()

	context = {
		'sellYourStartupBannerInst' : sellYourStartupBannerInst,
		'sellYourStartupBannerInstForm' : sellYourStartupBannerInstForm,
		'sellYourStartupUnparalleledExposureInst' : sellYourStartupUnparalleledExposureInst,
		'sellYourStartupUnparalleledExposureInstForm' : sellYourStartupUnparalleledExposureInstForm,
		'sellYourStartupBusinessListInst' : sellYourStartupBusinessListInst,
		'sellYourStartupBusinessListInstForm' : sellYourStartupBusinessListInstForm,
		'sellYourStartupBusinessWorthInst' : sellYourStartupBusinessWorthInst,
		'sellYourStartupBusinessWorthInstForm' : sellYourStartupBusinessWorthInstForm,
		'sellYourStartupFAQMainInst' : sellYourStartupFAQMainInst,
		'sellYourStartupFAQMainInstForm' : sellYourStartupFAQMainInstForm,
		'sellYourStartupFAQsInst' : sellYourStartupFAQsInst,
		'sellYourStartupFAQsInstForm' : sellYourStartupFAQsInstForm,
		'sellYourStartupExposureInst' : sellYourStartupExposureInst,
		'sellYourStartupExposureInstForm' : sellYourStartupExposureInstForm,
		'sellYourStartupDMInst':sellYourStartupDMInst,
		'sellYourStartupDMInstForm':sellYourStartupDMInstForm
	}
	return render(request, 'productPages/UI/sellYourStartup.html', context)

def sellYourStartupContactDMView(request):
	if request.method == 'POST':
		try:
			obj = sellYourStartupContactDM.objects.latest('id')
		except:
			obj = None
		objForm = sellYourStartupContactDMForm(request.POST, request.FILES, instance=obj)
		if objForm.is_valid():
			var = objForm.save()
			var.save()
			var.refresh_from_db()
			messages.success(request,'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('productPagesApp:sellYourStartupContactUrl')
	return HttpResponse('Invalid Entry')

def sellYourStartupContactUsBannerView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellYourStartupContactUsBanner, pk=pkID)
		objForm = sellYourStartupContactUsBannerForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellYourStartupContactUsKnowMoreView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellYourStartupContactUsKnowMore, pk=pkID)
		objForm = sellYourStartupContactUsKnowMoreForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellYourStartupContactUsKnowMoreFAQsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		pkID = request.POST.get('dataID')
		if methodType == 'new':
			objlnst = None
		else:
			objlnst = get_object_or_404(sellYourStartupContactUsKnowMoreFAQs, pk=pkID)
		objForm = sellYourStartupContactUsKnowMoreFAQsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

def sellYourStartupContactUsView(request):
	if request.method == 'POST':
		objForm = sellYourStartupContactUsForm(request.POST)
		redirectTo = request.POST.get('redirectTo')
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			# messages.success(request, 'Data sent for verification')
			redirectTo += '?success=true'
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


def sellYourStartupContactSignupView(request):

	try:
		sellYourStartupContactUsBannerInst = sellYourStartupContactUsBanner.objects.latest('id')

	except:
		sellYourStartupContactUsBannerInst = None
	sellYourStartupContactUsBannerInstForm = sellYourStartupContactUsBannerForm(instance=sellYourStartupContactUsBannerInst)

	try:
		sellYourStartupContactUsKnowMoreInst = sellYourStartupContactUsKnowMore.objects.latest('id')

	except:
		sellYourStartupContactUsKnowMoreInst = None
	sellYourStartupContactUsKnowMoreInstForm = sellYourStartupContactUsKnowMoreForm(instance=sellYourStartupContactUsKnowMoreInst)

	try:
		sellYourStartupContactDMInst = sellYourStartupContactDM.objects.latest('id')

	except:
		sellYourStartupContactDMInst = None


	sellYourStartupContactUsKnowMoreFAQsInst = sellYourStartupContactUsKnowMoreFAQs.objects.all().order_by('id')
	sellYourStartupContactUsKnowMoreFAQsInstForm = sellYourStartupContactUsKnowMoreFAQsForm()

	objForm = sellYourStartupContactUsForm()
	countryList = country.objects.all()
	context = {
		'sellYourStartupContactUsBannerInst' : sellYourStartupContactUsBannerInst,
		'sellYourStartupContactUsBannerInstForm' : sellYourStartupContactUsBannerInstForm,
		'sellYourStartupContactUsKnowMoreInst' : sellYourStartupContactUsKnowMoreInst,
		'sellYourStartupContactUsKnowMoreInstForm' : sellYourStartupContactUsKnowMoreInstForm,
		'sellYourStartupContactUsKnowMoreFAQsInst' : sellYourStartupContactUsKnowMoreFAQsInst,
		'sellYourStartupContactUsKnowMoreFAQsInstForm' : sellYourStartupContactUsKnowMoreFAQsInstForm,
		'sellYourStartupContactDMInst':sellYourStartupContactDMInst,
		'objForm':objForm,
		'countryList':countryList,
	}
	return render(request, 'productPages/UI/sellYourStartupContact.html', context)


