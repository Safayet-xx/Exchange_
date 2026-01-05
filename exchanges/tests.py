from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Session


class SessionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.requester = User.objects.create_user(email="requester@surrey.ac.uk", password="pass12345")
        self.helper = User.objects.create_user(email="helper@surrey.ac.uk", password="pass12345")

    def test_session_completion_transfers_credits(self):
        """Completing a session should transfer agreed credits from requester to helper."""
        # Wallets are created automatically by credits.signals
        requester_wallet = self.requester.wallet
        helper_wallet = self.helper.wallet
        initial_requester_balance = requester_wallet.balance
        initial_helper_balance = helper_wallet.balance

        sess = Session.objects.create(
            requester=self.requester,
            helper=self.helper,
            duration=Session.Duration.SIXTY,
            level=Session.Level.BEGINNER,
            status=Session.Status.ACCEPTED,
        )
        agreed = sess.agreed_amount  # auto-calculated on save

        sess.mark_completed(by_user=self.requester)

        requester_wallet.refresh_from_db()
        helper_wallet.refresh_from_db()
        self.assertEqual(requester_wallet.balance, initial_requester_balance - agreed)
        self.assertEqual(helper_wallet.balance, initial_helper_balance + agreed)

    def test_only_requester_can_mark_completed(self):
        sess = Session.objects.create(
            requester=self.requester,
            helper=self.helper,
            status=Session.Status.ACCEPTED,
        )
        with self.assertRaises(ValidationError):
            sess.mark_completed(by_user=self.helper)
