from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin


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


@admin.register(articleTagsOptions)
class articleTagsOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('description',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


@admin.register(categoryOptions)
class categoryOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('description',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


@admin.register(subCategoryOptions)
class subCategoryOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('description',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

@admin.register(blogArticles)
class blogArticlesImport(ImportExportModelAdmin):
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(articleDM)
