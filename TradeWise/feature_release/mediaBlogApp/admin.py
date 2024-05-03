from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin

#
def approvePost(modeladmin, request, queryset):
	for post in queryset:
		post.status = 'Published'
		post.save()
approvePost.short_description = 'Approve Selected'

#
def draftPost(modeladmin, request, queryset):
	for post in queryset:
		post.status = 'Draft'
		post.save()
draftPost.short_description = 'Draft Selected'

#
@admin.register(blogMedia)
class blogMediaImport(ImportExportModelAdmin, SummernoteModelAdmin):
	actions = [approvePost, draftPost,]
	summernote_fields = ('excerptContent', 'content2', 'content3', 'content4', 'content5')
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

admin.site.register(mediaBlogDM)