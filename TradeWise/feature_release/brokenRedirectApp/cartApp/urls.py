from django.urls import path
from . import views

app_name = 'cartApp'

urlpatterns = [
    path('pay/', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
    path('proceed-to-gateway/', views.process_to_pg_view, name='process_to_pg_url'),
]
