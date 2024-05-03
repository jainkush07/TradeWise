from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
import datetime
from django.db.models import Q
from taggit.models import Tag
from .forms import *
from .models import *
from blogHomeApp.models import newsCommonImageHomeModel


#
def searchBarView(request):
	query = request.GET.get('searchq')
	mediaObj = blogMedia.objects.all().order_by('-dateForMediaPost')
	if query:
		mediaSearchObj = mediaObj.filter(Q(title__icontains=query) | Q(subTitle__icontains=query) | Q(excerptContent__icontains=query) | Q(content2__icontains=query) | Q(content3__icontains=query) | Q(content4__icontains=query) | Q(content5__icontains=query)).distinct()
	else:
		mediaSearchObj = mediaObj
	return render(request, 'mediaBlog/UI/mediaList.html', {'mediaList':mediaSearchObj,})

#
def mediaListView(request):	
	mediaList = blogMedia.objects.all().order_by('-dateForMediaPost')
	createBlogMedia = blogMediaForm()
	try:
		latestDMInst = mediaBlogDM.objects.latest('id')
	except:
		latestDMInst = None	
	context = {
		'createBlogMedia': createBlogMedia,
		'mediaList' : mediaList,
		'latestDMInst':latestDMInst,
	}
	return render(request, 'mediaBlog/UI/mediaList.html', context)

#
def blogMediaView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(blogMedia, pk=pkID)
		objForm = blogMediaForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			if request.user.is_authenticated:
				cd.author = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Blog Media Sent For Verification')
		else:
			messages.error(request, 'Please Check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

#
def deleteFKdataView(request):
	if request.method == 'POST':
		deletePK = request.POST.get('deleteDataID')
		deleteFrom = request.POST.get('deleteFlag')
		requestedPage = request.POST.get('redirectTo')
		if deleteFrom == 'blogMedia':
			try:
				objInst = blogMedia.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')
		if deleteFrom == 'blogImageCategory':
			try:
				objInst = blogImageCategory.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')
		if deleteFrom == 'newsCommonImageHomeModel':
			try:
				objInst = newsCommonImageHomeModel.objects.get(pk=deletePK)
				objInst.delete()
				messages.success(request, 'Data Deleted')
			except:
				messages.error(request, 'Please Try Again Later')
		return redirect(requestedPage)
	return HttpResponse('Invalid Entry Point')

#
def mediaBlogDMView(request):
	if request.method == 'POST':
		try:
			objInst = mediaBlogDM.objects.latest('id')
		except:
			objInst = None
		objForm = mediaBlogDMForm(request.POST, request.FILES, instance=objInst)
		if objForm.is_valid():
			cd = objForm.save()
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'DM Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect('mediaBlogApp:mediaListURL')
	return HttpResponse('Invalid Entry')





