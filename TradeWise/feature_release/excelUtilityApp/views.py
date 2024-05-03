from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
# from datetime import date, datetime
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .forms import *

#
@staff_member_required
def upload_file_view(request):
	context = {}
	return render(request, 'excelUtility/file_upload.html', context)

#
def upload_file_submit_view(request):
	obj_form = uploaded_files_form(request.POST, request.FILES)
	context = {}
	if obj_form.is_valid():
		cd = obj_form.save()
		cd.author = request.user
		cd.save()
		context['errors'] = None
		context['success'] = True
		context['obj_id'] = cd.temp_code
	else:
		context['errors'] = f'{obj_form.errors}'
	return JsonResponse(context)

#
# check pan exist
# pan match excel email
# mobile match with excel
# check bank present if not then add
def process_sharebook_data_view(request):
	pass