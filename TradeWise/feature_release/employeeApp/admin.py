from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


def approvePost(modeladmin, request, queryset):
	for post in queryset:
		post.status = 'Published'
		post.save()
approvePost.short_description = 'Approve Selected'


def draftPost(modeladmin, request, queryset):
	for post in queryset:
		post.status = 'Draft'
		post.save()
draftPost.short_description = 'Draft Selected'

@admin.register(employeePersonalDetails)
class employeePersonalDetailsImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]


@admin.register(employeePermanentAddress)
class employeePermanentAddressImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(employeeLocalAddress)
class employeeLocalAddressImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(employeeCompanyDetails)
class employeeCompanyDetailsImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(employeeTypes)
class employeeTypesImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(employeeDepartment)
class employeeDepartmentImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(employeeRole)
class employeeRoleImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(employeeGrade)
class employeeGradeImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]


@admin.register(employeeDepartmentDetails)
class employeeDepartmentDetailsImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(employeeAccountType)
class employeeAccountTypeImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(uploadDocuments)
class uploadDocumentsImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(city)
class cityImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(state)
class cityImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(country)
class cityImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(companyDetailsFinancialObjs)
class cityImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(employeeBankDetailsObjs)
class cityImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]

@admin.register(employeeSalarySlips)
class cityImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]
