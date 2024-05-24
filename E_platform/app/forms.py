from django import forms
from .models import *
from django.utils import timezone
from .models import CustomeUser
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))

class UserForm(forms.ModelForm):
    class Meta:
        models = CustomeUser
        fields = ['username', 'email', 'password', 'user_type']  # Add or remove fields as needed

        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
            'user_type': 'User Type',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }


class AdminForm(forms.ModelForm):
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={'placeholder': 'Create Password'}))
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(
        attrs={'placeholder': 'Re-enter Password'}))
    DOB = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}))  # Ensure proper widget for DOB FIELD

    class Meta:
        model = Student
        fields = ['Full_Name', 'Mobile_no', 'EmailID',
                  'DOB', 'Gender', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'mobile_number', 'language', 'linkedin_profile', 'twitter_profile',
                  'facebook_profile']


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = CustomeUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomeUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None


class WorkExperienceForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = WorkExperience
        fields = ['company_name', 'position', 'start_date', 'end_date', 'description']


class EducationForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Education
        fields = ['institution_name', 'degree', 'field_of_study', 'start_date', 'end_date']


class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date', 'url']


class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = PrivacySettings
        fields = [
            'show_profile_to_logged_in_users',
            'show_courses_on_profile'
        ]
        labels = {
            'show_profile_to_logged_in_users': 'Show your profile page to logged-in users',
            'show_courses_on_profile': 'Show courses you\'re taking on your profile page'
        }


class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = NotificationSettings
        fields = ['promotion', 'helpful_resources', 'no_promotional_email']
        labels = {
            'promotion': 'Receive promotions and special offers',
            'helpful_resources': 'Receive helpful resources and course recommendations',
            'no_promotional_email': 'Do not send me any promotional emails'
        }


class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['friend_email']
        labels = {
            'friend_email': 'Friend\'s Email'
        }


