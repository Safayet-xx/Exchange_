from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['kind', 'title', 'skill_name', 'description']
        widgets = {
            'kind': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., "I can teach Python basics"'}),
            'skill_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., "Python"'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe what you can offer or what you need help with...'}),
        }
        labels = {
            'kind': 'Post Type',
            'title': 'Title',
            'skill_name': 'Skill',
            'description': 'Description',
        }
