from django import forms
from . models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class videoShortsCategoryOptionsForm(forms.ModelForm):
	class Meta:
		model = videoShortsCategoryOptions
		exclude = ('author', 'description', 'publish', 'created', 'updated', 'status')

class videoShortsSubCategoryOptionsForm(forms.ModelForm):
	class Meta:
		model = videoShortsSubCategoryOptions
		exclude = ('author', 'publish', 'created', 'updated', 'status', 'description')

class blogVideosShortsForm(forms.ModelForm):
	videoLink = forms.CharField(help_text='Enter Video ID only.')
	class Meta:
		model = blogVideosShorts
		fields = ('title', 'slug', 'excerptContent', 'tags', 'category', 'subCategory','relatedResearchReports', 'featuredShots','blogImage','videoLink', 'releaseDate',)
		widgets = {
			'relatedResearchReports': forms.CheckboxSelectMultiple(),
			'category': forms.CheckboxSelectMultiple(),
			'subCategory': forms.CheckboxSelectMultiple(),
            'releaseDate' : DateInput(),
		}

class blogVideosShortsDetailedForm(forms.ModelForm):
    class Meta:
        model = blogVideosShorts
        fields = ('subTitle', 'content1', 'content2', 'content3', 'content4','content5',)


class blogShortsListingDMForm(forms.ModelForm):
    class Meta:
        model = blogShortsListingDM
        exclude = ('publish', 'created', 'updated', 'status',)

class blogShortsDetailedDMForm(forms.ModelForm):
	class Meta:
		model = blogShortsDetailedDM
		exclude = ('blogProfileName', 'publish', 'created', 'updated', 'status',)



class shortsHeadingDMForm(forms.ModelForm):
	class Meta:
		model = shortsHeadingDM
		exclude = ('videoShorts', 'publish', 'created', 'updated', 'status')