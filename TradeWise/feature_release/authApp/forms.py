from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import *


class userPasswordCreateUpdateform(forms.ModelForm):
	class Meta:
		model = User
		fields = ('password',)
		

#
# class financialCompanyUpdatesForm(forms.ModelForm):
# 	class Meta:
# 		model = financialCompanyUpdates
# 		exclude = ['stockProfileName', 'publish', 'created', 'updated', 'status', 'analyst', 'verifiedBy']



class loginBannerObjectsForm(forms.ModelForm):
	class Meta:
		model = loginBannerObjects
		exclude = ('author','publish','created', 'updated', 'status', 'bannerImg')
		
