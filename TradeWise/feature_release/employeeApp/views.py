from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from stockApp.models import CURRENT_YEAR


#
def ajaxformView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(uploadDocuments, pk=pkID)
		objForm = uploadDocumentsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			# messages.success(request, 'Details sent for verification')
			return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
		else:
			# messages.error(request, 'Please check An Error occurred')
			return JsonResponse({'error': True, 'errors': form.errors})
	context = {}
	return render(request, 'employee/ajaxform.html', context)

#
@staff_member_required
def employeeListView(request):
	employeeProfiles = User.objects.filter(first_name='employeeProfile')
	context = {
		'employeeProfiles': employeeProfiles,
	}
	return render(request, 'employee/employeeList.html', context) 

#
def personalDetailView(request, slug=None):
	if slug:
		pageFlag = 'personalDetail'
		try:
			trackedProfileOwner = User.objects.get(username=slug)
			empPersonalDetailsInst = employeePersonalDetails.objects.get(profileOwner=trackedProfileOwner)
			profileSlug = trackedProfileOwner.username			
		except:
			return HttpResponse('Unauthorised Activity.')
		if empPersonalDetailsInst.firstName or empPersonalDetailsInst.lastName or empPersonalDetailsInst.profileImage or empPersonalDetailsInst.personalEmail or empPersonalDetailsInst.dateOfBirth or empPersonalDetailsInst.mobileNumber or empPersonalDetailsInst.gender or empPersonalDetailsInst.maritalStatus or empPersonalDetailsInst.educationDetails or empPersonalDetailsInst.highestQualification or empPersonalDetailsInst.uploadDegree or empPersonalDetailsInst.panNumber or empPersonalDetailsInst.uploadPan or empPersonalDetailsInst.aadharNumber or empPersonalDetailsInst.uploadAadhar :
			haveDataToEdit = True
		else:
			haveDataToEdit = False
		context = {
			'profileSlug': profileSlug,
			'pageFlag':pageFlag,
			'empPersonalDetailsInst': empPersonalDetailsInst,
			'haveDataToEdit': haveDataToEdit,
		}
		return render(request, 'employee/personalDetail.html', context)
	else:
		return HttpResponse('Invalid Entry')

#
def permanentAddressView(request, slug=None):
	if slug:
		pageFlag = 'permanentAddress'
		try:
			trackedProfileOwner = User.objects.get(username=slug)
			empPersonalDetailsInst = employeePermanentAddress.objects.get(profileOwner=trackedProfileOwner)
			profileSlug = trackedProfileOwner.username
		except:
			return HttpResponse('Unauthorised Activity.')
		# cityList = city.objects.all()
		# stateList = state.objects.all()
		# countryList = country.objects.all()
		countryList = country.objects.all()
		stateList = state.objects.filter(stateCountry=empPersonalDetailsInst.country)
		cityList = city.objects.filter(cityState=empPersonalDetailsInst.state)
		
		if empPersonalDetailsInst.address or empPersonalDetailsInst.city or empPersonalDetailsInst.pinCode or empPersonalDetailsInst.state or empPersonalDetailsInst.country or empPersonalDetailsInst.emergencyContactPersonName or empPersonalDetailsInst.emergencyContactPersonNumber:
			haveDataToEdit = True
		else:
			haveDataToEdit = False
		context = {
			'pageFlag':pageFlag,
			'profileSlug': profileSlug,
			'empPersonalDetailsInst': empPersonalDetailsInst,
			'cityList':cityList,
			'stateList' : stateList,
			'countryList' : countryList,
			'haveDataToEdit':haveDataToEdit,
		}
		return render(request, 'employee/permanentAddress.html', context)
	else:
		return HttpResponse('Invalid Entry')

#
def localAddressView(request, slug=None):
	if slug:
		pageFlag = 'localAddress'
		try:
			trackedProfileOwner = User.objects.get(username=slug)
			empPersonalDetailsInst = employeeLocalAddress.objects.get(profileOwner=trackedProfileOwner)
			profileSlug = trackedProfileOwner.username
		except:
			return HttpResponse('Unauthorised Activity.')
		try:
			permAddress = employeePermanentAddress.objects.get(profileOwner=trackedProfileOwner)
		except:
			permAddress = None
		countryList = country.objects.all()
		stateList = state.objects.filter(stateCountry=empPersonalDetailsInst.country)
		cityList = city.objects.filter(cityState=empPersonalDetailsInst.state)
		context = {
			'pageFlag':pageFlag,
			'profileSlug': profileSlug,
			'empPersonalDetailsInst': empPersonalDetailsInst,
			'cityList':cityList,
			'stateList' : stateList,
			'countryList' : countryList,
			'permAddress':permAddress,
		}
		return render(request, 'employee/localAddress.html', context)
	else:
		return HttpResponse('Invalid Entry')

#
def companyDetailView(request, slug='New'):
	employeeQuerySet = User.objects.filter(first_name='employeeProfile')
	userArray = []
	for item in employeeQuerySet:
		userArray.append(item.username)
	if slug == 'New':
		pageFlag = 'newID'
		profileSlug = 'New'
		print(pageFlag)
		context = {
			'pageFlag': pageFlag,
			'profileSlug':profileSlug,
			'userArray':userArray,
		}
	else:
		if slug:
			pageFlag = 'companyDetail'
			print(pageFlag)
			try:
				trackedProfileOwner = User.objects.get(username=slug)
				trackedProfileOwnerID = trackedProfileOwner.id 
				empPersonalDetailsInst = employeeCompanyDetails.objects.get(profileOwner=trackedProfileOwner)
				profileSlug = trackedProfileOwner.username
			except:
				return HttpResponse('Unauthorised Activity.')

			try:
				companyDetailsFinancialObjsInst = companyDetailsFinancialObjs.objects.filter(profileOwnerFK=trackedProfileOwner).order_by('-financialYear')
				createCompanyDetailsFinancial = companyDetailsFinancialObjsForm()
			except:
				companyDetailsFinancialObjsInst = None
				createCompanyDetailsFinancial = None

			context = {
				'trackedProfileOwnerID':trackedProfileOwnerID,
				'trackedProfileOwner':trackedProfileOwner,
				'pageFlag': pageFlag,
				'profileSlug': profileSlug,
				'empPersonalDetailsInst': empPersonalDetailsInst,
				'YEAR_CHOICES': YEAR_CHOICES,
				'CURRENT_YEAR': CURRENT_YEAR,
				'companyDetailsFinancialObjsInst':companyDetailsFinancialObjsInst,
				'createCompanyDetailsFinancial':createCompanyDetailsFinancial,
				'userArray':userArray,
			}		
		else:
			return HttpResponse('Invalid Entry')
	return render(request, 'employee/companyDetail.html', context)

#
def departmentDetailView(request, slug=None):
	if slug:
		pageFlag = 'departmentDetail'
		try:
			trackedProfileOwner = User.objects.get(username=slug)
			empPersonalDetailsInst = employeeDepartmentDetails.objects.get(profileOwner=trackedProfileOwner)
			profileSlug = trackedProfileOwner.username
		except:
			return HttpResponse('Unauthorised Activity.')

		employeeTypesInst = employeeTypes.objects.all()
		employeeDepartmentInst = employeeDepartment.objects.all()
		employeeRoleInst = employeeRole.objects.all()
		employeeGradeInst = employeeGrade.objects.all()
		if empPersonalDetailsInst.designation or empPersonalDetailsInst.employeeeType or empPersonalDetailsInst.department or empPersonalDetailsInst.role or empPersonalDetailsInst.grade or empPersonalDetailsInst.admin:
			haveDataToEdit = True
		else:
			haveDataToEdit = False
		context = {
			'pageFlag':pageFlag,
			'profileSlug': profileSlug,
			'empPersonalDetailsInst': empPersonalDetailsInst,
			'employeeTypesInst':employeeTypesInst,
			'employeeDepartmentInst':employeeDepartmentInst,
			'employeeRoleInst' : employeeRoleInst,
			'employeeGradeInst' : employeeGradeInst,
			'haveDataToEdit':haveDataToEdit,
		}
		return render(request, 'employee/departmentDetail.html', context)
	else:
		return HttpResponse('Invalid Entry')

#
def bankDetailView(request, slug=None):
	if slug:
		pageFlag = 'bankDetail'
		try:
			trackedProfileOwner = User.objects.get(username=slug)
			trackedProfileOwnerID = trackedProfileOwner.id 
			empPersonalDetailsInst = employeeBankDetailsObjs.objects.filter(profileOwnerFK=trackedProfileOwner).order_by('-setAsDefault','bankName')
			profileSlug = trackedProfileOwner.username
		except:
			return HttpResponse('Unauthorised Activity.')

		employeeAccountTypeInst = employeeAccountType.objects.all()

		createEmployeeBankDetails = employeeBankDetailsObjsForm()

		context = {
			'trackedProfileOwnerID':trackedProfileOwnerID,
			'pageFlag':pageFlag,
			'profileSlug': profileSlug,
			'empPersonalDetailsInst': empPersonalDetailsInst,
			'employeeAccountTypeInst':employeeAccountTypeInst,
			'createEmployeeBankDetails':createEmployeeBankDetails
		}
		return render(request, 'employee/bankDetail.html', context)
	else:
		return HttpResponse('Invalid Entry')

#
def documentUploadView(request, slug=None):
	if slug:
		pageFlag = 'documentUpload'
		try:
			trackedProfileOwner = User.objects.get(username=slug)
			empPersonalDetailsInst = uploadDocuments.objects.get(profileOwner=trackedProfileOwner)
			profileSlug = trackedProfileOwner.username
		except:
			return HttpResponse('Unauthorised Activity.')
		if empPersonalDetailsInst.offerLetter or empPersonalDetailsInst.experienceLetter or empPersonalDetailsInst.recommendationLetter or empPersonalDetailsInst.assetDocument:
			haveDataToEdit = True
		else:
			haveDataToEdit = False
		context = {
			'pageFlag':pageFlag,
			'profileSlug': profileSlug,
			'empPersonalDetailsInst': empPersonalDetailsInst,
			'haveDataToEdit':haveDataToEdit,
		}
		return render(request, 'employee/documentUpload.html', context)
	else:
		return HttpResponse('Invalid Entry')

#
def salarySlipView(request, slug=None):
	if slug:
		pageFlag = 'salarySlips'
		try:
			trackedProfileOwner = User.objects.get(username=slug)
			trackedProfileOwnerID = trackedProfileOwner.id 
		except:
			return HttpResponse('Unauthorised Activity.')
		salarySlips = employeeSalarySlips.objects.filter(profileOwnerFK=trackedProfileOwner).order_by('-year')
		salarySlipsDict = {}
		yearList = []
		for item in salarySlips:
			if item.year not in yearList:
				yearList.append(item.year)
		for item in yearList:
			salarySlipsDict[item] = salarySlips.filter(year=item)
		createSlipForm = employeeSalarySlipsForm()
		context = {
			'salarySlipsDict': salarySlipsDict,
			'yearList': yearList,
			'profileSlug': slug,
			'createSlipForm': createSlipForm,
			'trackedProfileOwnerID': trackedProfileOwnerID,
		}
		return render(request, 'employee/salarySlips.html', context)
	else:
		return HttpResponse('Invalid Entry')


#
def employeeUserCreationView(request):
	if request.method == 'POST':
		# if User.objects.filter(email=request.POST.get('email')).exists() or User.objects.filter(username=request.POST.get('empID')).exists():
		# 	error_msg = 'Employee with '+str(request.POST.get('email'))+' email address or with '+str(request.POST.get('empID'))+' employee ID already Exists.'
		# 	messages.error(request, error_msg)
		# 	return redirect('employeeApp:employeeListUrl')
		if request.POST.get('createOrUpdate') == 'create':
			if User.objects.filter(email=request.POST.get('email')).exists() or User.objects.filter(username=request.POST.get('empID')).exists():
				error_msg = 'Employee with '+str(request.POST.get('email'))+' email address or with '+str(request.POST.get('empID'))+' employee ID already Exists.'
				messages.error(request, error_msg)
				return redirect('employeeApp:employeeListUrl')
			try:
				user = User.objects.create_user(
					username=request.POST.get('empID'),
					# last_name=request.POST.get('mobileNo'),
					email=request.POST.get('email'),
					password=request.POST.get('password'),
					first_name='employeeProfile',
					is_staff=True,
					is_active=True
					)
				user.save()
			except:
				messages.error(request, 'Error while creating User')
				return redirect('employeeApp:companyDetailUrl')
			try:
				if user.last_name:
					cd1 = employeePersonalDetails.objects.create(profileOwner=user, mobileNumber=user.last_name)
				else:
					cd1 = employeePersonalDetails.objects.create(profileOwner=user)

				cd1.author = request.user
				cd1.save()
			except:
				messages.error(request, "Error while creating Personal Detail Attributes of Profile.")
			try:
				cd2 = employeePermanentAddress.objects.create(profileOwner=user)
				cd2.author = request.user
				cd2.save()
			except:
				messages.error(request, "Error while creating Permanent Address Attributes of Profile.")
			try:
				cd3 = employeeLocalAddress.objects.create(profileOwner=user)
				cd3.author = request.user
				cd3.save()
			except:
				messages.error(request, "Error while creating Local Address Attributes of Profile.")
			try:
				pf = request.POST.get('pfNumber')
				if not pf:
					pf = None
				jd = request.POST.get('joiningDate')
				if not jd:
					jd = None
				rd = request.POST.get('dateOfRelieving')
				if not rd:
					rd = None
				cd4 = employeeCompanyDetails.objects.create(
					profileOwner=user,
					pfNumber=pf,
					companyEmail=request.POST.get('email'),
					joiningDate=jd,
					dateOfRelieving=rd,
					author = request.user,
					)
				cd4.save()
			except:
				messages.error(request, "Error while creating Company Detail Attributes of Profile.")
			try:
				cd5 = employeeDepartmentDetails.objects.create(profileOwner=user)
				cd5.author = request.user
				cd5.save()
			except:
				messages.error(request, "Error while creating Department Attributes of Profile.")
			try:
				cd6 = uploadDocuments.objects.create(profileOwner=user)
				cd6.author = request.user
				cd6.save()
			except:
				messages.error(request, "Error while creating Document Attributes of Profile.")
				user.refresh_from_db()
			messages.success(request, 'User Profile Created. Now you can complete His/Her Profile. Also check If you see any error on screen while creating profile, Contact Support to resolve it.')
			slug = user.username
			return redirect('employeeApp:companyDetailUrl', slug)
		else:
			profileOwnerInst = get_object_or_404(User, pk=request.POST.get('ownerID'))
			slug = profileOwnerInst.username
			# if User.objects.filter(username=request.POST.get('empID')).exists():
			# 	errorMsg = str(request.POST.get('empID'))+' already present.'
			# 	messages.error(request, errorMsg)
			# 	return redirect('employeeApp:companyDetailUrl', slug)
			empUpdateForm = employeeCreationForm(request.POST, instance=profileOwnerInst)
			if empUpdateForm.is_valid():
				cd = empUpdateForm.save()
				cd.username=request.POST.get('empID')
				cd.email=request.POST.get('email')
				cd.save()
				# messages.success(request, 'Details has been updated Successfully.')
			else:
				messages.error(request, 'Unable to update email ID or Usename, Pls try again later.')
			companyDetailInst = get_object_or_404(employeeCompanyDetails, pk=request.POST.get('companyDetailID'))
			compDetailForm = employeeCompanyDetailsForm(request.POST, instance=companyDetailInst)
			if compDetailForm.is_valid():
				cdComp = compDetailForm.save()
				pf = request.POST.get('pfNumber')
				if not pf:
					pf = None
				jd = request.POST.get('joiningDate')
				if not jd:
					jd = None
				rd = request.POST.get('dateOfRelieving')
				if not rd:
					rd = None
				cdComp.profileOwner=profileOwnerInst
				cdComp.pfNumber=pf
				cdComp.companyEmail=request.POST.get('email')
				cdComp.joiningDate=jd
				cdComp.dateOfRelieving=rd
				cdComp.author = request.user
				cdComp.save()
				messages.success(request, 'Details has been updated Successfully.')
			else:
				messages.error(request, 'Unable to update PF, Joining Date or Date of Relieving, Pls try again later.')
			return redirect('employeeApp:companyDetailUrl', slug)
	return HttpResponse('Invalid Entry')


#Form Submitted#
#
def employeePersonalDetailsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		redirectSuccess = request.POST.get('redirecting')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(employeePersonalDetails, pk=pkID)  #change model name
		objForm = employeePersonalDetailsForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
			return redirect(redirectTo)
		return redirect('employeeApp:permanentAddressUrl',slug=redirectSuccess)
	return HttpResponse('Invalid Entry')

#
def employeePermanentAddressView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		redirectSuccess = request.POST.get('redirecting')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(employeePermanentAddress, pk=pkID)  #change model name
		objForm = employeePermanentAddressForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
			return redirect(redirectTo)
		return redirect('employeeApp:localAddressUrl',slug=redirectSuccess)
	return HttpResponse('Invalid Entry')


#
def employeeLocalAddressView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		redirectSuccess = request.POST.get('redirecting')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(employeeLocalAddress, pk=pkID)  #change model name
		objForm = employeeLocalAddressForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
			return redirect(redirectTo)
		return redirect('employeeApp:departmentDetailUrl',slug=redirectSuccess)
	return HttpResponse('Invalid Entry')


#
def employeeCompanyDetailsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		yearUnique = request.POST.get('financialYear')
		redirectSuccess = request.POST.get('redirecting')

		parentPK = request.POST.get('profileOwnerFK')
		parentInstance = get_object_or_404(User,pk=parentPK)
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(employeeCompanyDetails, pk=pkID)  #change model name
		objForm = employeeCompanyDetailsForm(request.POST, request.FILES, instance=objlnst) #change form name		
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Upper Form Details sent for verification')
		else:
			messages.error(request, 'Bottom Form Details An Error occurred')
		if not yearUnique:
			pass
		elif companyDetailsFinancialObjs.objects.filter(profileOwnerFK= parentInstance, financialYear= yearUnique).exists():
			messages.error(request, 'Data for year already present')
		else:
			objFormForeign = companyDetailsFinancialObjsForm(request.POST, request.FILES)
			if objFormForeign.is_valid():
				cd = objFormForeign.save(commit=False)
				cd.createdBy = request.user
				cd.profileOwnerFK = parentInstance
				cd.save()
				cd.refresh_from_db()
				messages.success(request, 'Details sent for verification')
			else:
				messages.error(request, 'Please check An Error occurred')
				return redirect(redirectTo)
		return redirect('employeeApp:departmentDetailUrl',slug=redirectSuccess)
	return HttpResponse('Invalid Entry')

#
def employeeCompanyDetailsBelowView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		yearUnique = request.POST.get('financialYear')
		redirectSuccess = request.POST.get('redirecting')
		parentPK = request.POST.get('profileOwnerFK')
		parentInstance = get_object_or_404(User,pk=parentPK)
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(companyDetailsFinancialObjs, pk=pkID)  #change model name
		objFormForeign = companyDetailsFinancialObjsForm(request.POST, request.FILES, instance=objlnst)
		if not yearUnique:
			messages.error(request, 'Year Not Selected.')
		elif companyDetailsFinancialObjs.objects.filter(profileOwnerFK= parentInstance, financialYear= yearUnique).exists() and not objlnst:
			messages.error(request, 'Data for year already present')
		else:
			if objFormForeign.is_valid():
				cd = objFormForeign.save(commit=False)
				cd.createdBy = request.user
				cd.profileOwnerFK = parentInstance
				cd.save()
				cd.refresh_from_db()
				messages.success(request, 'Details sent for verification')
			else:
				messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Unauthorised Activity!')

#
def companyDetailsFinancialObjsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(companyDetailsFinancialObjs, pk=pkID)  #change model name
		objForm = companyDetailsFinancialObjsForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


#
def employeeTypesView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(employeeTypes, pk=pkID)  #change model name
		objForm = employeeTypesForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


#
def employeeDepartmentView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(employeeDepartment, pk=pkID)  #change model name
		objForm = employeeDepartmentForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


#
def employeeRoleView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(employeeRole, pk=pkID)  #change model name
		objForm = employeeRoleForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


#
def employeeGradeView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(employeeGrade, pk=pkID)  #change model name
		objForm = employeeGradeForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')


#
def employeeDepartmentDetailsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		redirectSuccess = request.POST.get('redirecting')
		empProfileStatus = request.POST.get('account')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(employeeDepartmentDetails, pk=pkID)
		# if objlnst:
		# 	profileUser = objlnst.profileOwner
		# 	if profileUser.is_active and empProfileStatus == 'activate':
		# 		pass
		# 	else:
		# 		cd = profileUser
		# 		cd.is_active = False
		# 		cd.save()
		objForm = employeeDepartmentDetailsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, objForm.errors)
			return redirect(redirectTo)
		return redirect('employeeApp:bankDetailUrl',slug=redirectSuccess)
	return HttpResponse('Invalid Entry')


#
def employeeAccountTypeView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(employeeAccountType, pk=pkID)  #change model name
		objForm = employeeAccountTypeForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Details sent for verification')
		else:
			messages.error(request, 'Please check An Error occurred')
			return redirect(redirectTo)
		return redirect('employeeApp:bankDetailUrl')
	return HttpResponse('Invalid Entry')


#
def employeeBankDetailsObjsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		redirectSuccess = request.POST.get('redirecting')
		parentPK = request.POST.get('profileOwnerFK')
		parentInstance = get_object_or_404(User,pk=parentPK)
		if methodType == 'new':
			objlnst = None
			messageReq = 'Bank Details created Successfully.'			
		else:
			pkID = request.POST.get('dataID')
			messageReq = 'Bank Details updated Successfully.'
			objlnst = get_object_or_404(employeeBankDetailsObjs, pk=pkID)  #change model name
		objForm = employeeBankDetailsObjsForm(request.POST, request.FILES, instance=objlnst) #change form name
		if objForm.is_valid():
			if request.POST.get('setAsDefault'):
				allRelatedObjs = employeeBankDetailsObjs.objects.filter(profileOwnerFK=parentInstance)
				for item in allRelatedObjs:
					item.setAsDefault = False
					item.save()
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.profileOwnerFK = parentInstance
			cd.save()
			cd.refresh_from_db()
			messages.success(request, messageReq)
		else:
			messages.error(request, 'An Error occurred. Please check for any possible error.')
		return redirect(redirectTo)
	return HttpResponse('Invalid Entry')
		
#
def ajaxFormUploadView(request):
	if request.method == 'POST':		
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(uploadDocuments, pk=pkID)
		form = uploadDocumentsForm(data=request.POST, files=request.FILES, instance=objlnst)
		if form.is_valid():
			cd = form.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			# print 'valid form'
			return redirect('employeeApp:employeeListUrl')
		else:
			# print 'invalid form'
			# print form.errors
			messages.error(request, 'Please check An Error occurred')
			return redirect(redirectTo)
	return HttpResponseRedirect('/ingest/')

#
def uploadDocumentsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(uploadDocuments, pk=pkID)  #change model name
		print(f'request.POST: {request.POST}')
		print(f'request.FILES: {request.FILES}')
		print(f'objlnst: {objlnst}')
		objForm = uploadDocumentsForm(request.POST, request.FILES, instance=objlnst) #change form name
		print(objForm)
		if objForm.is_valid():
			print(f'this is form inside --- {objForm}')
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			objlnst = get_object_or_404(uploadDocuments, pk=pkID)			
			offerLetterUrl = objlnst.offerLetter or False
			experienceLetterUrl = objlnst.experienceLetter or False
			recommendationLetterUrl = cd.recommendationLetter or False
			assetDocumentUrl = cd.assetDocument or False

			appraisalLetterUrl = cd.assetDocument or False
			probationConfirmationUrl = cd.probationConfirmation or False
			# relievingLetterUrl = cd.relievingLetter or False
			# misconductLetterUrl = cd.misconductLetter or False
			return JsonResponse({
				'error': False,
				'message': 'Uploaded Successfully',
				'offerLetterUrl': str(offerLetterUrl),
				'experienceLetterUrl': str(experienceLetterUrl),
				'recommendationLetterUrl': str(recommendationLetterUrl),
				'assetDocumentUrl': str(assetDocumentUrl),
				'appraisalLetterUrl': str(appraisalLetterUrl),
				'probationConfirmationUrl': str(probationConfirmationUrl),
				# 'relievingLetterUrl':str(relievingLetterUrl),
				# 'misconductLetterUrl':str(misconductLetterUrl),
			})
			# return redirect('employeeApp:employeeListUrl')
		else:
			# messages.error(request, 'Please check An Error occurred')
			print('else block')
			return JsonResponse({'error': True, 'errors': form.errors})
			# return redirect(redirectTo)
	return HttpResponse('Invalid Entry')

#
def ajaxformView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(uploadDocuments, pk=pkID)
		objForm = uploadDocumentsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.save()
			cd.refresh_from_db()
			# messages.success(request, 'Details sent for verification')
			return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
		else:
			# messages.error(request, 'Please check An Error occurred')
			return JsonResponse({'error': True, 'errors': form.errors})
	context = {}
	return render(request, 'employee/ajaxform.html', context)




#
def employeeSalarySlipsView(request):
	if request.method == 'POST':
		methodType = request.POST.get('submitType')
		redirectTo = request.POST.get('requestFrom')
		redirectSuccess = request.POST.get('redirecting')
		parentPK = request.POST.get('profileOwnerFK')
		parentInstance = get_object_or_404(User,pk=parentPK)
		if methodType == 'new':
			objlnst = None
		else:
			pkID = request.POST.get('dataID')
			objlnst = get_object_or_404(employeeSalarySlips, pk=pkID)
		objForm = employeeSalarySlipsForm(request.POST, request.FILES, instance=objlnst)
		if objForm.is_valid():
			cd = objForm.save(commit=False)
			cd.createdBy = request.user
			cd.profileOwnerFK = parentInstance
			cd.save()
			cd.refresh_from_db()
			messages.success(request, 'Salary Slip Data sent for verification')
		else:
			messages.error(request, 'Bottom Form Details An Error occurred')
			return redirect(redirectTo)
		return redirect('employeeApp:salarySlipUrl',slug=redirectSuccess)
	return HttpResponse('Invalid Entry')


#
def employeeProfilePictureView(request):
	if request.method == 'POST':
		requestFrom = request.POST.get('requestFrom')
		pkID = request.POST.get('dataUser')
		objlnst = get_object_or_404(User, username=pkID)
		empProfInst = get_object_or_404(employeePersonalDetails, profileOwner=objlnst)
		if request.user == objlnst:
			objForm = employeeProfilePictureForm(request.POST, request.FILES, instance=empProfInst)
			if objForm.is_valid():
				cd = objForm.save()
				cd.save()
				cd.refresh_from_db()
				messages.success(request, 'Profile Pic Updated Successfully.')
			else:
				messages.error(request, 'An Error occurred. Try again later or Contact Support.')
		else:
			return HttpResponse('Invalid Action.')
		return redirect(requestFrom)
	return HttpResponse('Invalid Entry.')