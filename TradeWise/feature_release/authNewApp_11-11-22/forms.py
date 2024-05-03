from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import *


class otp_authentication_form(forms.ModelForm):
	class Meta:
		model = otp_authentication
		exclude = ('userProfile', 'author', 'publish', 'created', 'updated', 'status',)