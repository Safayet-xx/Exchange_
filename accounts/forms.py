from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()

# Allowed university email domains
ALLOWED_EMAIL_DOMAINS = {"brunel.ac.uk", "ucl.ac.uk", "imperial.ac.uk"}  # add more if needed


class SignUpForm(UserCreationForm):
    """
    Flexible sign-up form for swapped User models.
    - If USERNAME_FIELD == "email": we do NOT add a second 'email' field.
    - If USERNAME_FIELD != "email" and the model has an 'email' attribute:
      we add an optional 'email' field.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        username_field = UserModel.USERNAME_FIELD
        if hasattr(UserModel, "email") and username_field != "email":
            self.fields["email"] = forms.EmailField(
                required=False,  # change to True if you want it mandatory
                help_text="Optional — used for verification and notifications.",
            )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        # Make sure the username field matches your User model
        fields = (UserModel.USERNAME_FIELD,)  # password1/password2 are auto-added

    def clean_username(self):
        """
        Validate the user's email domain (assuming USERNAME_FIELD is 'email').
        """
        email = self.cleaned_data.get("email") or self.cleaned_data.get("username")
        if not email:
            return email
        domain = (email.split("@")[-1] or "").lower()
        if domain not in ALLOWED_EMAIL_DOMAINS:
            raise forms.ValidationError("Please use a verified university email address.")
        return email

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        # Copy email if it's not the username field
        if "email" in self.cleaned_data and UserModel.USERNAME_FIELD != "email":
            try:
                setattr(
                    user,
                    "email",
                    self.cleaned_data.get("email", "") or getattr(user, "email", ""),
                )
            except Exception:
                pass
        if commit:
            user.save()
        return user
