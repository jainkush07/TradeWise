from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin


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


@admin.register(blogVideos)
class blogVideosImport(ImportExportModelAdmin, SummernoteModelAdmin):
	list_display = ('title', 'author', 'explore', 'releasedDate',)
	list_filter = ('author', 'explore', 'releasedDate', )
	search_fields = ('author', 'title', 'explore', 'releasedDate',)
	summernote_fields = ('content',)
	actions = [approvePost, draftPost,]
	def save_model(self, request, obj, form, change):
		obj.analyst = request.user
		super().save_model(request, obj, form, change)

@admin.register(videoBlogHits)
class videoBlogHitsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = ('videoBlog', 'hitBy', 'created',)
	list_filter = ('videoBlog', 'hitBy', 'created', )
	search_fields = ('videoBlog', 'hitBy', 'created',)

admin.site.register(marketingData)
admin.site.register(videoBlogGenericData)
admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(blogPageSectionsOrdering)
admin.site.register(blogVideoListingDM)
admin.site.register(blogVideoDetailedDM)
admin.site.register(videosHeadingDM)



