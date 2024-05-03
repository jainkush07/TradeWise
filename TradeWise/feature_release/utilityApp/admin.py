from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import *


#
@admin.register(excel_utility)
class excel_utility_admin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = ('mobile','full_payment_date','pre_ipo_stock','quantity','final_amount','owned_by','source',)
	list_filter = ('owned_by','source',)
	search_fields = ('mobile','full_payment_date','pre_ipo_stock','quantity','final_amount','owned_by','source',)

	def save_model(self, request, obj, form, change):
		obj.author = request.user
		super().save_model(request, obj, form, change)