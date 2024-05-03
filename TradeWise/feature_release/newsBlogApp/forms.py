from django import forms
from . models import *
from mptt.forms import TreeNodeChoiceField

class DateInput(forms.DateInput):
	input_type = 'date'


class blogNewsForm(forms.ModelForm):
	content1 = forms.CharField(widget=forms.Textarea(attrs={'class':'summernotefield'}), required=False)
	# content2 = forms.CharField(widget=forms.Textarea(attrs={'class':'summernotefield'}), required=False)
	# content3 = forms.CharField(widget=forms.Textarea(attrs={'class':'summernotefield'}), required=False)
	# content4 = forms.CharField(widget=forms.Textarea(attrs={'class':'summernotefield'}), required=False)
	# content5 = forms.CharField(widget=forms.Textarea(attrs={'class':'summernotefield'}), required=False)
	class Meta:
		model = blogNews
		exclude = ('author','publish','created','updated', 'status','content2','content3','content4','content5')
		widgets = {
			'relatedResearchReports': forms.CheckboxSelectMultiple(),
			'dateOfNews': DateInput(),
			'timeOfNews': forms.TimeInput(attrs={'type': 'time'}),
		}

class blogNewsListingDMForm(forms.ModelForm):
	class Meta:
		model = blogNewsListingDM
		exclude = ('publish', 'created', 'updated', 'status')

class blogNewsDetailedDMForm(forms.ModelForm):
	class Meta:
		model = blogNewsDetailedDM
		exclude = ('blogProfileName','publish', 'created', 'updated', 'status')

class blogWebNewsListingDMForm(forms.ModelForm):
	class Meta:
		model = blogWebNewsListingDM
		exclude = ('publish', 'created', 'updated', 'status')


class newsHeadingDMForm(forms.ModelForm):
	class Meta:
		model = newsHeadingDM
		exclude = ('newsBlog', 'publish', 'created', 'updated', 'status')

class newsHeadingWebDMForm(forms.ModelForm):
	class Meta:
		model = newsHeadingWebDM
		exclude = ('newsBlog', 'publish', 'created', 'updated', 'status')