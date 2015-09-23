from django import forms
from django.contrib.auth.models import User

#Infinity
class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label=(u'User Name'))
    email = forms.EmailField(label=(u'Email Address'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(
        render_value=False))
    password1 = forms.CharField(
        label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
