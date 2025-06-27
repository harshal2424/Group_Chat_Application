from django import forms
from .models import Message
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [ 'message','file']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']
        
        
class UserCreationFormWithProfile(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, help_text="")
    first_name = forms.CharField(max_length=30, required=True, help_text="")
    last_name = forms.CharField(max_length=30, required=True, help_text="")
    email = forms.EmailField(required=True, help_text="")
    avatar = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'first_name', 'last_name', 'email', 'avatar')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Enter your first name.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Enter your last name.")
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']