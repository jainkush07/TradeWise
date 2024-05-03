from django import forms
from . models import *
from mptt.forms import TreeNodeChoiceField

class DateInput(forms.DateInput):
    input_type = 'date'

class articleTagsOptionsForm(forms.ModelForm):
	class Meta:
		model = articleTagsOptions
		exclude = ('author', 'description', 'publish', 'created', 'updated', 'status')

class categoryOptionsForm(forms.ModelForm):
	class Meta:
		model = categoryOptions
		exclude = ('author', 'publish', 'created', 'updated', 'status', 'description')

class subCategoryOptionsForm(forms.ModelForm):
	class Meta:
		model = subCategoryOptions
		exclude = ('author', 'publish', 'created', 'updated', 'status','description')

class blogArticlesForm(forms.ModelForm):
    class Meta:
        model = blogArticles
        fields = ('title', 'slug', 'excerptContent', 'articleImage', 'category', 'subCategory','relatedResearchReports', 'dateForListing', 'tags', )
        widgets = {
            'dateForListing': DateInput(),
            'category': forms.CheckboxSelectMultiple(),
            'subCategory': forms.CheckboxSelectMultiple(),
            'relatedResearchReports': forms.CheckboxSelectMultiple(),
        }
class blogArticlesDetailedForm(forms.ModelForm):
    class Meta:
        model = blogArticles
        fields = ('subTitle', 'content1', 'content2', 'content3', 'content4','content5')
        widgets = {
            'dateForListing': DateInput(),
            'category': forms.CheckboxSelectMultiple(),
            'subCategory': forms.CheckboxSelectMultiple(),
        }
   


# class CommentForm(forms.ModelForm):
#     parent = TreeNodeChoiceField(queryset=Comment.objects.all())

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields['parent'].widget.attrs.update(
#             {'class': 'd-none'})
#         self.fields['parent'].label = ''
#         self.fields['parent'].required = False

#     class Meta:
#         model = Comment
#         fields = ('name', 'parent', 'content')

#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
#             'content': forms.Textarea(attrs={'class': 'form-control'}),
#         }

#     def save(self, *args, **kwargs):
#         Comment.objects.rebuild()
#         return super(newCommentForm, self).save(*args, **kwargs)


#
class articleDMForm(forms.ModelForm):
    class Meta:
        model = articleDM
        exclude = ('author', 'publish', 'created', 'updated', 'status')