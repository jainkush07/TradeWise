from django.shortcuts import render, redirect, HttpResponse
from .forms import metaDetailForDMForm
from django.contrib import messages
from .models import *


def metaDetailForDMView(request):
	if request.method == 'POST':
		redirectTo = request.POST.get('requestFrom')
		objID = request.POST.get('dataID')
		typeOfRequest = request.POST.get('requestType')
		staticPage = request.POST.get('static_page')
		if objID and typeOfRequest == 'update':
			objInst = metaDetailForDM.objects.get(pk=objID)
		else:
			objInst = None
		objForm = metaDetailForDMForm(request.POST, request.FILES, instance= objInst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.author = request.user
			cd.save()
			cd.refresh_from_db()
			objForm.save_m2m()
			messages.success(request, 'Meta Detail Updated Successfully.')
		else:
			messages.error(request, f'Kindly check following errors or Contact Support. {objForm.errors}')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')