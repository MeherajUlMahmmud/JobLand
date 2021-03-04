from django import forms
from django.contrib.auth.forms import authenticate
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Email or Password is incorrect")


class ApplicantRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address')
    name = forms.CharField(max_length=60)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text='Password must contain at least 8 character including numeric values',
    )
    is_applicant = forms.BooleanField(initial=True)
    check = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2", "is_applicant", "check")


class CompanyRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address')
    name = forms.CharField(max_length=60)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text='Password must contain at least 8 character including numeric values',
    )
    is_company = forms.BooleanField(initial=True)
    check = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2", "is_company", "check")


class ApplicantEditProfileForm(ModelForm):
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
    )
    resume = forms.FileField(
        required=False,
        error_messages={'invalid': "Pdf files only"},
        widget=forms.FileInput,
    )
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ApplicantProfileModel
        fields = '__all__'
        exclude = ['user']


class ApplicantAddPhoneNumberForm(ModelForm):
    class Meta:
        model = ApplicantProfileModel
        fields = ('phone',)


class ApplicantAddSocialForm(ModelForm):
    class Meta:
        model = ApplicantProfileModel
        fields = ('linkedin', 'github', 'twitter', 'facebook')


class ApplicantAddResumeForm(ModelForm):
    resume = forms.FileField(required=False, error_messages={'invalid': "Pdf files only"}, widget=forms.FileInput)

    class Meta:
        model = ApplicantProfileModel
        fields = ('resume',)


class WorkExperienceForm(ModelForm):
    started = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    left = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = WorkExperienceModel
        fields = '__all__'
        exclude = ['user']


class EducationForm(ModelForm):
    started = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = EducationModel
        fields = '__all__'
        exclude = ['user']


class SkillSetForm(ModelForm):
    class Meta:
        model = SkillSetModel
        fields = '__all__'
        exclude = ['user']


class LanguageSetForm(ModelForm):
    class Meta:
        model = LanguageModel
        fields = '__all__'
        exclude = ['user']


class ReferenceForm(ModelForm):
    class Meta:
        model = ReferenceModel
        fields = '__all__'
        exclude = ['user']


class AwardForm(ModelForm):
    class Meta:
        model = AwardModel
        fields = '__all__'
        exclude = ['user']


class PreferredJobForm(ModelForm):
    class Meta:
        model = PreferredJobModel
        fields = '__all__'
        exclude = ['user']


class CompanyEditProfileForm(ModelForm):
    image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    logo = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CompanyProfileModel
        fields = '__all__'
        exclude = ['user']


class RatingForm(ModelForm):
    class Meta:
        model = RatingModel
        fields = ('extra', 'comments',)


class AccountInformationForm(ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email')


class AuthenticationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('password',)
