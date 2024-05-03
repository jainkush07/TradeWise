from django import forms
from django.db import models
from .models import *

#
class metaDetailForDMForm(forms.ModelForm):
	# helper = forms.FormHelper()
	# helper.layout = Layout(
	# 	Div(
	# 		Field('meta_title', wrapper_class='col-md-6'),
	# 		Field('meta_description', wrapper_class='col-md-6'),
	# 		Field('meta_keywords', wrapper_class='col-md-6'),
	# 		Field('featured_image', wrapper_class='col-md-6'),
	# 	css_class='form-row') 
	# )
	class Meta:
		model = metaDetailForDM
		exclude = ['end_point', 'author', 'publish', 'created', 'updated', 'status',]
	# def __init__(self, *args, **kwargs):
	# 	super(metaDetailForDMForm, self).__init__(*args, **kwargs)
	# 	for visible in self.visible_fields():
	# 		visible.field.widget.attrs['class'] = 'col-md-6'