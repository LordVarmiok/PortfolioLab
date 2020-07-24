from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User


# class Email(forms.EmailField):
#     def clean(self, value):
#         super(Email, self).clean(value)
#         try:
#             User.objects.get(email=value)
#             raise forms.ValidationError("Email already in use. Try another one.")
#         except User.DoesNotExist:
#             return value
#
#
# class UserRegistrationForm(forms.Form):
#     first_name = forms.CharField(widget=forms)
#     password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
#     password2 = forms.CharField(widget=forms.PasswordInput(), label="Repeat the password")
#
#     email = Email()
#
#     def clean_password(self):
#         if self.data['password1'] != self.data['password2']:
#             raise forms.ValidationError('Passwords do not match')
#         return self.data['password1']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_username(self):
        return self.cleaned_data['email']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']