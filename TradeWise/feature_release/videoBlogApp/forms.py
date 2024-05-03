from django import forms
from . models import *
from mptt.forms import TreeNodeChoiceField

class DateInput(forms.DateInput):
	input_type = 'date'

class categoryOptionsForm(forms.ModelForm):
	class Meta:
		model = categoryOptions
		exclude = ('author', 'description', 'publish', 'created', 'updated', 'status')

class subCategoryOptionsForm(forms.ModelForm):
	class Meta:
		model = subCategoryOptions
		exclude = ('author', 'publish', 'created', 'updated', 'status', 'description')

class blogVideosForm(forms.ModelForm):
	class Meta:
		model = blogVideos
		exclude = ('author', 'publish', 'created', 'updated', 'status','subTitle','content','blogVideo','totalHits', 'totalHitsXDays',)
		widgets = {
			'relatedResearchReports': forms.CheckboxSelectMultiple(),
			'category': forms.CheckboxSelectMultiple(),
			'subCategory': forms.CheckboxSelectMultiple(),
			'releasedDate': DateInput()
		}

class blogVideoListingDMForm(forms.ModelForm):
	class Meta:
		model = blogVideoListingDM
		exclude = ('blogProfileName','publish', 'created', 'updated', 'status')

class blogVideoDeatiledDMForm(forms.ModelForm):
	class Meta:
		model = blogVideoDetailedDM
		exclude = ('blogProfileName','publish', 'created', 'updated', 'status')

class videoBlogGenericDataForm(forms.ModelForm):
	class Meta:
		model = videoBlogGenericData
		exclude = ('author', 'publish', 'created', 'updated', 'status')


class blogVideosDetailedForm(forms.ModelForm):
	class Meta:
		model = blogVideos
		fields = ('subTitle', 'content',)


class newCommentForm(forms.ModelForm):
	parent = TreeNodeChoiceField(queryset=Comment.objects.all())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['parent'].widget.attrs.update({'class': 'd-none'})
		self.fields['parent'].label = ''
		self.fields['parent'].required = False

	class Meta:
		model = Comment
		fields = ('name', 'parent', 'content')

	widgets = {
		'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
		'content': forms.Textarea(attrs={'class': 'form-control'}),
	}

	def save(self, *args, **kwargs):
		Comment.objects.rebuild()
		return super(newCommentForm, self).save(*args, **kwargs)


class blogPageSectionsOrderingForm(forms.ModelForm):
	class Meta:
		model = blogPageSectionsOrdering
		fields = '__all__'


class videosHeadingDMForm(forms.ModelForm):
	class Meta:
		model = videosHeadingDM
		exclude = ('videoBlog', 'publish', 'created', 'updated', 'status')