from django import forms
from .models import *
from django.contrib.auth.models import User


#
class employeeCreationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'last_name', 'email',)

#
class employeePersonalDetailsForm(forms.ModelForm):
	class Meta:
		model = employeePersonalDetails
		exclude = ('profileOwner','author','publish','created','updated','status', 'lastName')

#
class employeeProfilePictureForm(forms.ModelForm):
	class Meta:
		model = employeePersonalDetails
		fields = ('profileImage',)

#
class employeePermanentAddressForm(forms.ModelForm):
	class Meta:
		model = employeePermanentAddress
		exclude = ('profileOwner','author','publish','created','updated','status')

#
class employeeLocalAddressForm(forms.ModelForm):
	class Meta:
		model = employeeLocalAddress
		exclude = ('profileOwner','author','publish','created','updated','status')

#
class employeeCompanyDetailsForm(forms.ModelForm):
	class Meta:
		model = employeeCompanyDetails
		exclude = ('profileOwner','author','publish','created','updated','status')

#
class companyDetailsFinancialObjsForm(forms.ModelForm):
	class Meta:
		model = companyDetailsFinancialObjs
		exclude = ('profileOwnerFK','author','publish','created','updated','status')

#
class employeeTypesForm(forms.ModelForm):
	class Meta:
		model = employeeTypes
		exclude = ('publish','created','updated','status')

#
class employeeDepartmentForm(forms.ModelForm):
	class Meta:
		model = employeeDepartment
		exclude = ('publish','created','updated','status')

#
class employeeRoleForm(forms.ModelForm):
	class Meta:
		model = employeeRole
		exclude = ('publish','created','updated','status')

#
class employeeGradeForm(forms.ModelForm):
	class Meta:
		model = employeeGrade
		exclude = ('publish','created','updated','status')

#
class employeeDepartmentDetailsForm(forms.ModelForm):
	class Meta:
		model = employeeDepartmentDetails
		exclude = ('profileOwner','author','publish','created','updated','status')
		
#
class employeeAccountTypeForm(forms.ModelForm):
	class Meta:
		model = employeeAccountType
		exclude = ('publish','created','updated','status')

# #
# class employeeBankDetailsForm(forms.ModelForm):
# 	class Meta:
# 		model = employeeBankDetails
# 		exclude = ('profileOwner','author','publish','created','updated','status')

#
class employeeBankDetailsObjsForm(forms.ModelForm):
	class Meta:
		model = employeeBankDetailsObjs
		exclude = ('profileOwnerFK','author','publish','created','updated','status')

#
class uploadDocumentsForm(forms.ModelForm):
	class Meta:
		model = uploadDocuments
		exclude = ('profilePhoto', 'profileOwner', 'author','publish','created','updated','status')


#
class employeeSalarySlipsForm(forms.ModelForm):
	class Meta:
		model = employeeSalarySlips
		exclude = ('profileOwnerFK','author','publish','created','updated','status')
