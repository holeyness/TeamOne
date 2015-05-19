# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class PostForm(forms.Form):
    title = forms.CharField(label='title', max_length = 200, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label='description', max_length = 300, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    post_image = forms.FileField(required=False)


class LoginForm(forms.Form):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})) 

class SignupForm(forms.Form):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})) 
    email = forms.CharField(label = 'email', max_length = 150, widget=forms.TextInput(attrs={'class':'form-control'}))
    poster_bool = forms.BooleanField(required=False)