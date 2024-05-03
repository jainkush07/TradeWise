
from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin

# Register your models here.

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


@admin.register(videoShortsCategoryOptions)
class categoryOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('description',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


@admin.register(videoShortsSubCategoryOptions)
class subCategoryOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('description',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


@admin.register(blogVideosShorts)
class blogVideosImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('content1','content2','content3','content4','content5',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)


admin.site.register(blogShortsListingDM)
admin.site.register(blogShortsDetailedDM)
admin.site.register(shortsHeadingDM)



