from django import forms
from django.db import models
from .models import *

#
class uploaded_files_form(forms.ModelForm):
	class Meta:
		model = uploaded_files
		exclude = ['author', 'publish', 'created', 'updated', 'status',]