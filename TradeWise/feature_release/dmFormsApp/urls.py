from django.urls import path
from . import views

app_name = 'dmFormsApp'

urlpatterns = [
	path('dm-only-form/', views.metaDetailForDMView, name='metaDetailForDMUrl'),
]
