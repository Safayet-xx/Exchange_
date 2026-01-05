from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Profile


class ProfileTests(TestCase):
    def test_profile_auto_created_on_user_create(self):
        """A Profile should be created automatically via signals when a User is created."""
        User = get_user_model()
        user = User.objects.create_user(email="testuser@surrey.ac.uk", password="pass12345")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_str_uses_full_name_when_present(self):
        """__str__ should return a friendly name when available."""
        User = get_user_model()
        user = User.objects.create_user(email="another@surrey.ac.uk", password="pass12345")
        profile = user.profile  # created by signal
        profile.full_name = "Test User"
        profile.save()
        self.assertEqual(str(profile), "Test User")
