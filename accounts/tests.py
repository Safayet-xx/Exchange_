from django.test import TestCase

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from accounts.views import generate_otp_code, is_otp_expired


class OTPTests(TestCase):
    """Tests for OTP helper functions."""

    def test_otp_generation(self):
        """Test that OTP is generated with 6 digits"""
        otp = generate_otp_code()
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())

    def test_otp_expiration(self):
        """Test that OTP expiration works"""
        created_at = timezone.now() - timedelta(minutes=20)
        self.assertTrue(is_otp_expired(created_at, expiry_minutes=10))

    def test_otp_not_expired(self):
        """Test that fresh OTP is not expired"""
        created_at = timezone.now() - timedelta(minutes=2)
        self.assertFalse(is_otp_expired(created_at, expiry_minutes=10))
