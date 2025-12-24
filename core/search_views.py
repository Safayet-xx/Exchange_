from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from accounts.models import User
from skills.models import UserSkill, Skill
from profiles.models import Profile
from posts.models import Post


@login_required
def unified_search_view(request):
    """
    Unified search page - search for users, skills, or posts
    """
    search_type = request.GET.get('type', 'posts')  # 'posts', 'users', or 'skills'
    query = request.GET.get('q', '').strip()
    department = request.GET.get('department', '')
    
    results = []
    context = {
        'search_type': search_type,
        'query': query,
        'department': department,
        'departments': UserSkill.DEPARTMENTS,
    }
    
    # Get department name for display
    if department:
        dept_dict = dict(UserSkill.DEPARTMENTS)
        context['department_name'] = dept_dict.get(department, department)
    
    if query:
        if search_type == 'posts':
            # Search for posts (exclude posts from staff/superusers)
            posts = Post.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(skill_name__icontains=query)
            ).exclude(
                Q(user__is_superuser=True) | Q(user__is_staff=True)
            ).select_related('user__profile').order_by('-created_at')
            
            # Filter by department if specified
            if department:
                posts = posts.filter(user__user_skills__department=department).distinct()
            
            results = posts[:20]
            
        elif search_type == 'users':
            # Search for users (exclude superusers and staff)
            users = User.objects.filter(
                Q(profile__display_name__icontains=query) |
                Q(profile__full_name__icontains=query) |
                Q(profile__handle__icontains=query) |
                Q(email__icontains=query)
            ).exclude(
                Q(is_superuser=True) | Q(is_staff=True)
            ).select_related('profile').distinct()
            
            # Filter by department if specified
            if department:
                users = users.filter(user_skills__department=department).distinct()
            
            results = users[:20]
            
        elif search_type == 'skills':
            # Search for user skills (exclude staff/superusers)
            user_skills = UserSkill.objects.filter(
                Q(skill__name__icontains=query) |
                Q(description__icontains=query)
            ).exclude(
                Q(user__is_superuser=True) | Q(user__is_staff=True)
            ).select_related('user', 'user__profile', 'skill')
            
            # Filter by department if specified
            if department:
                user_skills = user_skills.filter(department=department)
            
            results = user_skills[:20]
    
    context['results'] = results
    context['result_count'] = len(results)
    
    return render(request, 'search/unified_search.html', context)


@login_required
def request_session_view(request, user_skill_id):
    """
    Request a session based on a user skill found in search
    """
    user_skill = get_object_or_404(UserSkill, id=user_skill_id)
    
    # Redirect to session creation with pre-filled data
    return redirect(f"/exchanges/create/?skill={user_skill.skill.id}&helper={user_skill.user.id}")
