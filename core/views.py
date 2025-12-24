from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q

from posts.models import Post

User = get_user_model()


def home_view(request):
    """
    Public home page.

    - If user is logged in: show dashboard with recent activity
    - If user is not logged in: show landing page
    """
    context = {}
    
    if request.user.is_authenticated:
        # Get recent posts (exclude staff/superuser posts)
        recent_posts = Post.objects.exclude(
            Q(user__is_superuser=True) | Q(user__is_staff=True)
        ).select_related('user__profile').order_by('-created_at')[:6]
        
        # Get upcoming sessions if they exist
        try:
            from exchanges.models import Session
            upcoming_sessions = Session.objects.filter(
                Q(seeker=request.user) | Q(helper=request.user),
                status='pending'
            ).select_related('skill', 'seeker__profile', 'helper__profile').order_by('scheduled_at')[:3]
        except:
            upcoming_sessions = []
        
        context = {
            'recent_posts': recent_posts,
            'upcoming_sessions': upcoming_sessions,
            'sessions_count': len(upcoming_sessions),
        }
    
    return render(request, "core/home.html", context)
