from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *

#
# def redirectView(request, slug=None):
# 	if slug:
# 		try:
# 			redirectToObj = redirectBucket.objects.get(source=slug)
# 		except:
# 			redirectToObj = None
# 		if redirectToObj:
# 			return redirect(redirectToObj.destination)
# 	return redirect('handler404Url')


def redirectAddEditView(request):
	createredirectBucketForm = redirectBucketForm()
	redirectToObjs = redirectBucket.objects.all().order_by('source')
	context = {
		'createredirectBucketForm': createredirectBucketForm,
		'redirectToObjs': redirectToObjs,
	}
	return render(request, 'redirectHTML/redirectListAdd.html', context)

#
def redirectBucketSubmitView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(redirectBucket, pk=pkID)
		objForm = redirectBucketForm(request.POST, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Data sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')



