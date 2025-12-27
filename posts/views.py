from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Post
from .forms import PostForm


@login_required
def post_list(request):
    """Browse all posts - Marketplace (excludes staff/superuser posts)"""
    query = request.GET.get('q', '').strip()
    kind_filter = request.GET.get('kind', '')
    
    posts = Post.objects.filter(is_active=True).exclude(
        Q(user__is_superuser=True) | Q(user__is_staff=True)
    ).select_related('user', 'user__profile')
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(skill_name__icontains=query)
        )
    
    if kind_filter in ['offer', 'want']:
        posts = posts.filter(kind=kind_filter)
    
    return render(request, 'posts/list.html', {
        'posts': posts,
        'query': query,
        'kind_filter': kind_filter,
    })


@login_required
def post_create(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('posts:list')
    else:
        form = PostForm()
    
    return render(request, 'posts/create.html', {'form': form})


@login_required
def post_detail(request, pk):
    """View a single post"""
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save(update_fields=['views'])
    
    return render(request, 'posts/detail.html', {'post': post})


@login_required
def my_posts(request):
    """View user's own posts"""
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'posts/my_posts.html', {'posts': posts})


@login_required
def post_delete(request, pk):
    """Delete a post"""
    post = get_object_or_404(Post, pk=pk, user=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('posts:my_posts')
    
    return render(request, 'posts/delete.html', {'post': post})
