from django.urls import path
from .  import views

app_name = 'stockPriceApp'

urlpatterns = [
	path('', views.marketDashboardView, name="marketDashboardUrl"),
]
