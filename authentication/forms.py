from django import forms
from django.core.exceptions import ValidationError
from .models import User

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label=None,required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter username...'}))
    email = forms.EmailField(label=None, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter email...'}))
    password1 = forms.CharField(label=None,widget=forms.PasswordInput(attrs={'placeholder': 'Enter password...'}))
    password2 = forms.CharField(label=None, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password...'}))


    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username =forms.CharField(
        label=None,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username...'
        })
    )
    password=forms.CharField(
        label=None,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password...'
        })
    )

    class Meta:
        model= User
        fields = ('username', 'password')
        labels ={
            'username': None,
            'password': None,
        }

    def clean(self):
        username =self.cleaned_data.get('username')
        password =self.cleaned_data.get('password')
        if not User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username does not exist.")
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise ValidationError("Incorrect password.")
        return self.cleaned_data
                        