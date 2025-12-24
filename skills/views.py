from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill, UserSkill, SkillCategory
from .forms import UserSkillForm


@login_required
def my_skills(request):
    """View and manage user's skills"""
    user_skills = UserSkill.objects.filter(user=request.user).select_related('skill', 'skill__category')
    categories = SkillCategory.objects.all()
    
    return render(request, 'skills/my_skills.html', {
        'user_skills': user_skills,
        'categories': categories,
    })


@login_required
def add_skill(request):
    """Add a skill to user's profile"""
    if request.method == 'POST':
        form = UserSkillForm(request.POST)
        if form.is_valid():
            user_skill = form.save(commit=False)
            user_skill.user = request.user
            user_skill.save()
            messages.success(request, f'Added {user_skill.skill.name} to your skills!')
            return redirect('skills:my_skills')
    else:
        form = UserSkillForm()
    
    return render(request, 'skills/add_skill.html', {'form': form})


@login_required
def edit_skill(request, pk):
    """Edit a skill"""
    user_skill = get_object_or_404(UserSkill, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = UserSkillForm(request.POST, instance=user_skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('skills:my_skills')
    else:
        form = UserSkillForm(instance=user_skill)
    
    return render(request, 'skills/edit_skill.html', {'form': form, 'user_skill': user_skill})


@login_required
def delete_skill(request, pk):
    """Delete a skill"""
    user_skill = get_object_or_404(UserSkill, pk=pk, user=request.user)
    
    if request.method == 'POST':
        skill_name = user_skill.skill.name
        user_skill.delete()
        messages.success(request, f'Removed {skill_name} from your skills!')
        return redirect('skills:my_skills')
    
    return render(request, 'skills/delete_skill.html', {'user_skill': user_skill})


@login_required
def browse_skills(request):
    """Browse all available skills"""
    category_id = request.GET.get('category')
    query = request.GET.get('q', '').strip()
    
    skills = Skill.objects.all().prefetch_related('user_skills__user')
    
    if category_id:
        skills = skills.filter(category_id=category_id)
    
    if query:
        skills = skills.filter(name__icontains=query)
    
    categories = SkillCategory.objects.all()
    
    return render(request, 'skills/browse.html', {
        'skills': skills,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })
