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
from gifts.models import Donation


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = ['categories','quantity', 'categories']


class ArchiveForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['is_taken']


class ContactForm(forms.Form):
    # first_name = forms.CharField(required=True, max_length=254)
    # last_name = forms.CharField(required=True, max_length=254)
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True, max_length=254)
    message = forms.CharField(required=True, max_length=254)


class SecondDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = ['is_taken']