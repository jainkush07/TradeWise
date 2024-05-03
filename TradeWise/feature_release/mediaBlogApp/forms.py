from django import forms
from . models import *
from mptt.forms import TreeNodeChoiceField

class DateInput(forms.DateInput):
    input_type = 'date'

class blogMediaForm(forms.ModelForm):
    class Meta:
        model = blogMedia
        exclude = ['author', 'verifiedBy','publish', 'created', 'updated', 'status' ]
        widgets = {
            'dateForMediaPost': DateInput()
        }

class mediaBlogDMForm(forms.ModelForm):
    class Meta:
        model = mediaBlogDM
        exclude = ['publish', 'created', 'updated', 'status' ]