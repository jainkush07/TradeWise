from django.urls import path
from . import views

app_name = 'excelUtilityApp'

urlpatterns = [
	path('upload_api_v1/', views.upload_file_submit_view, name="upload_file_submit_url"),
	path('', views.upload_file_view, name="upload_file_url"),
]