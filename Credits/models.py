from django.db import models, transaction as dbtx
from django.conf import settings
from django.core.exceptions import ValidationError

class CreditWallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")
    balance = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"Wallet({self.user_id}) = {self.balance}"

class CreditTransaction(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="credits_sent")
    to_user   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="credits_received")
    amount    = models.PositiveIntegerField()
    note      = models.CharField(max_length=255, blank=True)
    session   = models.ForeignKey("exchanges.Session", on_delete=models.SET_NULL, null=True, blank=True, related_name="credit_transactions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TX {self.id}: {self.from_user_id} -> {self.to_user_id} ({self.amount})"

def get_wallet(user):
    return CreditWallet.objects.select_for_update().get(user=user)

def transfer_credits(*, from_user, to_user, amount, note="", session=None):
    if amount <= 0:
        raise ValidationError("Amount must be positive.")
    if from_user == to_user:
        raise ValidationError("Cannot transfer credits to yourself.")

    with dbtx.atomic():
        from_w = get_wallet(from_user)
        to_w = get_wallet(to_user)

        if from_w.balance < amount:
            raise ValidationError("Insufficient balance.")

        from_w.balance -= amount
        to_w.balance += amount
        from_w.save(update_fields=["balance"])
        to_w.save(update_fields=["balance"])

        tx = CreditTransaction.objects.create(
            from_user=from_user,
            to_user=to_user,
            amount=amount,
            note=note,
            session=session,
        )
        return tx
