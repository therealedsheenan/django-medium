from django import forms
from blog.models import Comment, Post
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = [
            'author',
            'title',
            'text'
        ]

        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = [
            'author',
            'text'
        ]

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }
