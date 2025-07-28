from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import ManagerProfile

class ManagerCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    department = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            manager_profile = ManagerProfile.objects.get(user=user)
            manager_profile.phone = self.cleaned_data['phone']
            manager_profile.department = self.cleaned_data['department']
            manager_profile.save()
        return user

class ManagerEditForm(UserChangeForm):
    phone = forms.CharField(max_length=20, required=False)
    department = forms.CharField(max_length=100, required=False)
    password = None  # Remove password field from the form

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'managerprofile'):
            self.fields['phone'].initial = self.instance.managerprofile.phone
            self.fields['department'].initial = self.instance.managerprofile.department

    def save(self, commit=True):
        user = super().save(commit=commit)
        if hasattr(user, 'managerprofile'):
            user.managerprofile.phone = self.cleaned_data['phone']
            user.managerprofile.department = self.cleaned_data['department']
            user.managerprofile.save()
        return user

class ManagerPasswordResetForm(SetPasswordForm):
    """Form for admins to set/reset manager passwords"""
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].help_text = "Le nouveau mot de passe pour ce manager."
        self.fields['new_password2'].help_text = "Confirmez le nouveau mot de passe."


class UserSettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Adresse email')
    first_name = forms.CharField(required=True, label='Prénom')
    last_name = forms.CharField(required=True, label='Nom')
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Cette adresse email est déjà utilisée.')
        return email
