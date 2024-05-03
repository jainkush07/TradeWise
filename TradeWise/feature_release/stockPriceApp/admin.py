from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(stockDailyUpdates)
class stockDailyUpdatesImport(ImportExportModelAdmin):
	def save_model(self, request, obj, form, change):
		obj.author = request.user
		super().save_model(request, obj, form, change)