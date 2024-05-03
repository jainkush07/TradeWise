from django import forms
from .models import *


#
class tagModelForm(forms.ModelForm):
	class Meta:
		model = tagModel
		exclude = ('publish','created','updated')

#
class categoryImageModelForm(forms.ModelForm):
	class Meta:
		model = categoryImageModel
		exclude = ('publish','created','updated')

#
class newsCommonImageHomeModelForm(forms.ModelForm):
	class Meta:
		model = newsCommonImageHomeModel
		exclude = ('publish','created','updated')

#
class homeBlogDMForm(forms.ModelForm):
	class Meta:
		model = homeBlogDM
		exclude = ('publish','created','updated')


