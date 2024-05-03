from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
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


@admin.register(blogNews)
class articleTagsOptionsImport(ImportExportModelAdmin, SummernoteModelAdmin):
	summernote_fields = ('content1', 'content2', 'content3', 'content4', 'content5')
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)



admin.site.register(blogNewsListingDM)
admin.site.register(blogNewsDetailedDM)
admin.site.register(blogWebNewsListingDM)
admin.site.register(newsHeadingDM)
admin.site.register(newsHeadingWebDM)

