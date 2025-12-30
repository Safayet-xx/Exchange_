from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

# Model + form
try:
    from .models import Profile
except Exception:
    Profile = None

try:
    from .forms import ProfileSetupForm
except Exception:
    ProfileSetupForm = None


# --------- Profile setup (private) ---------
@login_required
def profile_setup_view(request):
    # Ensure profile exists
    try:
        p = request.user.profile
    except Exception:
        messages.error(request, "Could not load your profile; please re-login.")
        return redirect("accounts:logout")

    # If you don’t have a ModelForm yet, fall back to a simple POST handler
    if ProfileSetupForm is None:
        if request.method == "POST":
            # Minimal fallback save
            p.display_name = request.POST.get("display_name", p.display_name)
            p.handle = request.POST.get("handle", p.handle)
            p.full_name = request.POST.get("full_name", p.full_name)
            p.is_completed = True
            p.save()
            messages.success(request, "Profile completed. Welcome to Exchange!")
            return redirect("core:home")
        return render(request, "profiles/profile_setup.html", {})

    # Proper form flow
    if request.method == "POST":
        form = ProfileSetupForm(request.POST, instance=p)
        if form.is_valid():
            prof = form.save(commit=False)
            prof.is_completed = True
            prof.save()
            messages.success(request, "Profile completed. Welcome to Exchange!")
            return redirect("core:home")
        messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileSetupForm(instance=p)

    return render(request, "profiles/profile_setup.html", {"form": form})


# --------- Public profile (required by exchange/urls.py) ---------
def public_profile_view(request, handle: str):
    """
    Renders a public profile page by handle.
    This exists so exchange/urls.py can import it safely.
    """
    if Profile is None:
        # Render a minimal page if model is missing
        return render(request, "profiles/public_profile.html", {"p": None})

    profile = get_object_or_404(Profile, handle__iexact=handle)
    return render(request, "profiles/public_profile.html", {"profile": profile})


# --------- User search (required by exchange/urls.py) ---------
def user_search_view(request):
    """
    Basic user search over handle/full_name.
    This exists so exchange/urls.py can import it safely.
    """
    q = (request.GET.get("q") or "").strip()
    results = []
    if Profile and q:
        results = (
            Profile.objects
            .filter(Q(handle__icontains=q) | Q(full_name__icontains=q))
            .select_related("user")[:50]
        )
    return render(request, "profiles/user_search.html", {"q": q, "results": results})
