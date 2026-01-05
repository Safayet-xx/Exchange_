from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import CreditWallet, CreditTransaction, transfer_credits

User = get_user_model()

@login_required
def wallet_view(request):
    """View user's credit wallet and transaction history"""
    wallet, created = CreditWallet.objects.get_or_create(user=request.user)
    
    # Get transactions where user sent credits
    txs_sent = CreditTransaction.objects.filter(
        from_user=request.user
    ).select_related('to_user').order_by('-created_at')
    
    # Get transactions where user received credits
    txs_received = CreditTransaction.objects.filter(
        to_user=request.user
    ).select_related('from_user').order_by('-created_at')
    
    # Combine and sort all transactions
    all_txs = list(txs_sent) + list(txs_received)
    all_txs.sort(key=lambda x: x.created_at, reverse=True)
    
    return render(request, "credits/wallet.html", {
        "wallet": wallet,
        "transactions": all_txs,
        "txs_sent": txs_sent,
        "txs_received": txs_received,
    })


@login_required
def transfer_view(request):
    """Transfer credits to another user.
    
    NOTE: Manual transfers are disabled for regular users.
    Credits now move automatically when a session is completed.
    """
    # Block manual transfers for non-admin users
    if not request.user.is_staff:
        messages.error(request, "Manual credit transfers are disabled. Credits move automatically after sessions.")
        return redirect("credits:wallet")

    # Pre-fill form from GET parameters
    initial_to = (request.GET.get("to") or "").strip()
    initial_amount = (request.GET.get("amount") or "").strip()
    initial_note = (request.GET.get("note") or "").strip()

    context = {
        "suggested_users": User.objects.exclude(
            id=request.user.id
        ).filter(
            email_verified=True
        ).select_related("profile")[:10],
        "to_email": initial_to,
        "amount": initial_amount,
        "note": initial_note,
    }

    if request.method == "POST":
        to_email = request.POST.get("to_email", "").strip().lower()
        try:
            amount = int(request.POST.get("amount", "0"))
        except ValueError:
            messages.error(request, "Please enter a valid amount.")
            context.update({"to_email": to_email, "amount": request.POST.get("amount", ""), "note": request.POST.get("note", "")})
            return render(request, "credits/transfer.html", context)

        note = request.POST.get("note", "").strip()

        # Validate inputs
        if not to_email:
            messages.error(request, "Please enter recipient's email.")
            context.update({"to_email": to_email, "amount": amount, "note": note})
            return render(request, "credits/transfer.html", context)

        if amount <= 0:
            messages.error(request, "Amount must be greater than 0.")
            context.update({"to_email": to_email, "amount": amount, "note": note})
            return render(request, "credits/transfer.html", context)

        try:
            # Find recipient user
            to_user = User.objects.get(email__iexact=to_email)

            # Perform transfer
            transfer_credits(
                from_user=request.user,
                to_user=to_user,
                amount=amount,
                note=note,
            )

            messages.success(request, f"Successfully transferred {amount} credits to {to_email}.")
            return redirect("credits:wallet")

        except User.DoesNotExist:
            messages.error(request, f"User with email '{to_email}' not found.")
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Transfer failed: {str(e)}")

        # Re-render with posted values
        context.update({"to_email": to_email, "amount": amount, "note": note})
        return render(request, "credits/transfer.html", context)

    # GET request
    return render(request, "credits/transfer.html", context)
