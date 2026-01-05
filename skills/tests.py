from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from .models import SkillCategory, Skill, UserSkill


class UserSkillTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email="skilluser@surrey.ac.uk", password="pass12345")
        self.cat = SkillCategory.objects.create(name="Programming", icon="code", description="Coding skills")
        self.skill = Skill.objects.create(name="Python", category=self.cat)

    def test_create_user_skill(self):
        """Creating a UserSkill should link a user to a skill with metadata."""
        us = UserSkill.objects.create(
            user=self.user,
            skill=self.skill,
            department="computer_science",
            proficiency_level="beginner",
            years_of_experience=1.0,
            description="I can help with Python basics",
        )
        self.assertEqual(us.user, self.user)
        self.assertEqual(us.skill, self.skill)
        self.assertIn("Python", str(us))
        self.assertIn("skilluser@surrey.ac.uk", str(us))

    def test_user_skill_unique_per_user_and_skill(self):
        """UserSkill is unique per (user, skill)."""
        UserSkill.objects.create(user=self.user, skill=self.skill)
        with self.assertRaises(IntegrityError):
            UserSkill.objects.create(user=self.user, skill=self.skill)
