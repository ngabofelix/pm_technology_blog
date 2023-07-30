from django import forms
from .models import Posts, Topics
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title','content','slug','published','post_topic','image']

class TopicsCreationForm(forms.ModelForm):
    class Meta:
        model = Topics
        fields = ['name']

class UsersRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']