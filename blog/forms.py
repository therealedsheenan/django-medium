from django import forms
from blog.models import Comment, Post


class PostForm(forms.ModelForm):
    author = forms.TextInput(attrs={
        'class': 'input'
    })

    title = forms.TextInput(attrs={
        'class': 'input'
    })

    text = forms.Textarea(attrs={
        'class': 'input'
    })

    class Meta():
        model = Post
        fields = [
            'author',
            'title',
            'text'
        ]


class CommentForm(forms.ModelForm):
    author = forms.TextInput(attrs={
        'class': 'input'
    })

    text = forms.Textarea(attrs={
        'class': 'input'
    })

    class Meta():
        model = Comment
        fields = [
            'author',
            'text'
        ]
