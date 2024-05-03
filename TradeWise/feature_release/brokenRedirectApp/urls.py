from django.urls import path
from . import views

app_name = 'brokenRedirectApp'

urlpatterns = [
    path('', views.redirectAddEditView, name="redirectAddEditUrl"),
    path('redirect-bucket-submit/', views.redirectBucketSubmitView, name="redirectBucketSubmitUrl"),
]
