from django import forms

from .models import customUser
from django.contrib.auth.forms import UserCreationForm

class customUserForm(UserCreationForm):
    class Meta:
        model = customUser
        fields = [
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'email',
            'phone',
            'username',
            'password1',
            'password2',
            ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Last Name'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your Email ID'}),
            'phone': forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter valid Phone Number'}),
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter unique username'}),
            'gender':forms.RadioSelect(choices=[['male','Male'],['female','Female']]),
            'date_of_birth': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'password1': forms.TextInput(attrs={'class':'form-control','type':'password','placeholder':'Enter valid password'}),
            'password2': forms.TextInput(attrs={'class':'form-control','type':'password','placeholder':'Enter your password to verify'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'gender': 'Gender',
            'date_of_birth': 'Date of Birth',
            'email': 'Email',
            'phone': 'Phone',
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

class identifyUserForm(forms.Form):
    username_or_email = forms.CharField(max_length=100,label='Username or Email',
                                        widget=forms.TextInput(attrs={'class':'form-control',
                                                                      'placeholder':'Enter the username or email address',
                                                                      }))

class OTPForm(forms.Form):
    otp = forms.IntegerField(label='Enter OTP',widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Your OTP'}))