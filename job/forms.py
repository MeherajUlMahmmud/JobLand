from django import forms
from .models import *
from django.forms import ModelForm


class PostJobForm(ModelForm):
    image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    is_active = forms.BooleanField(initial=True)

    class Meta:
        model = JobModel
        fields = '__all__'
        exclude = ['user']


class ApplicationForm(ModelForm):
    class Meta:
        model = AppliedJobModel
        fields = ()


class JobFilledForm(ModelForm):
    class Meta:
        model = FilledJobModel
        fields = ()
