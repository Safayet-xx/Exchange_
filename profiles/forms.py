from django import forms
from .models import Profile

class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "display_name", "handle", "full_name", "role",
            "bio", "university", "hobbies", "fun_fact"
        ]
        widgets = {
            "display_name": forms.TextInput(attrs={"placeholder": "Display name", "class": "form-control"}),
            "handle": forms.TextInput(attrs={"placeholder": "unique-handle", "class": "form-control"}),
            "full_name": forms.TextInput(attrs={"placeholder": "Full name", "class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"placeholder": "Tell us about yourself...", "class": "form-control", "rows": 3}),
            "university": forms.TextInput(attrs={"placeholder": "e.g., Brunel University", "class": "form-control"}),
            "hobbies": forms.TextInput(attrs={"placeholder": "e.g., Reading, Coding, Gaming", "class": "form-control"}),
            "fun_fact": forms.Textarea(attrs={"placeholder": "Share something interesting about yourself!", "class": "form-control", "rows": 2}),
        }
        help_texts = {
            "handle": "Choose a unique username (letters, numbers, hyphens only)",
            "role": "Select whether you are a student or professor",
        }
        labels = {
            "display_name": "Display Name",
            "handle": "Username/Handle",
            "full_name": "Full Name",
            "role": "Role",
            "bio": "About Me",
            "university": "University",
            "hobbies": "Hobbies",
            "fun_fact": "Fun Fact",
        }
