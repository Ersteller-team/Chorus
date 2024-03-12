from django import forms
from django.contrib.auth.models import User
from .models import ProfileData

class ProfileForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    
    class Meta():
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password'
        }
        widgets = {
            'icon': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'spotify_access_token': forms.TextInput(attrs={'class': 'form-control'}),
            'spotify_refresh_token': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddProfileForm(forms.ModelForm):
    
    class Meta():
        model = ProfileData
        fields = ['icon', 'description', 'spotify_access_token', 'spotify_refresh_token']
        labels = {
            'icon': 'Icon',
            'description': 'Description',
            'spotify_id': 'Spotify ID',
            'spotify_access_token': 'Spotify Access Token',
            'spotify_refresh_token': 'Spotify Refresh Token',
        }
