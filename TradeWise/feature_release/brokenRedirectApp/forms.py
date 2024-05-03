from django import forms
from .models import *



class redirectBucketForm(forms.ModelForm):
	class Meta:
		model = redirectBucket
		fields = '__all__'
