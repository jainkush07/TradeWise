from django.urls import path
from . import views

app_name = 'employeeApp'

urlpatterns = [
	path('', views.employeeListView, name="employeeListUrl"),
	path('employee-user-creation', views.employeeUserCreationView, name="employeeUserCreationUrl"),
	path('personal-info', views.employeePersonalDetailsView, name='employeePersonalDetailsUrl'),	
	path('permanent-address', views.employeePermanentAddressView, name='employeePermanentAddressUrl'),
	path('local-address', views.employeeLocalAddressView, name='employeeLocalAddressUrl'),
	path('company-info', views.employeeCompanyDetailsView, name='employeeCompanyDetailsUrl'),
	path('company-info-below', views.employeeCompanyDetailsBelowView, name='employeeCompanyDetailsBelowUrl'),
	path('company-info-financial', views.companyDetailsFinancialObjsView, name='companyDetailsFinancialObjsUrl'),
	path('emp-type', views.employeeTypesView, name='employeeTypesUrl'),
	path('department', views.employeeDepartmentView, name='employeeDepartmentUrl'),
	path('role', views.employeeRoleView, name='employeeRoleUrl'),
	path('grade', views.employeeGradeView, name='employeeGradeUrl'),
	path('departmental-details', views.employeeDepartmentDetailsView, name='employeeDepartmentDetailsUrl'),
	path('account-type', views.employeeAccountTypeView, name='employeeAccountTypeUrl'),
	path('bank-details', views.employeeBankDetailsObjsView, name='employeeBankDetailsObjsUrl'),
	path('profile-pic-update', views.employeeProfilePictureView, name='employeeProfilePictureUrl'),
	# path('bank-details-obj', views.employeeBankDetailsObjsView, name='employeeBankDetailsObjsUrl'),
	path('upload-documents', views.uploadDocumentsView, name='uploadDocumentsUrl'),
	path('salary-slip-objects', views.employeeSalarySlipsView, name='employeeSalarySlipsUrl'),
	path('ajax/form', views.ajaxformView, name="ajaxformUrl"),
	path('ajax/upload', views.ajaxFormUploadView, name="ajaxFormUploadUrl"),
	path('<slug:slug>/personal-details', views.personalDetailView, name='personalDetailUrl'),
	path('<slug:slug>/permanent-address', views.permanentAddressView, name='permanentAddressUrl'),
	path('<slug:slug>/local-details', views.localAddressView, name='localAddressUrl'),
	path('New/company-details', views.companyDetailView, name='companyDetailUrl'),
	path('<slug:slug>/company-details/', views.companyDetailView, name='companyDetailUrl'),
	path('<slug:slug>/department-details/', views.departmentDetailView, name='departmentDetailUrl'),
	path('<slug:slug>/bank-details/', views.bankDetailView, name='bankDetailUrl'),
	path('<slug:slug>/document-upload/', views.documentUploadView, name='documentUploadUrl'),
	path('<slug:slug>/salary-slips/', views.salarySlipView, name='salarySlipUrl'),
]