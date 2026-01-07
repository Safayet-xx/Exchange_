from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Session

User = get_user_model()


@login_required
def session_list_view(request):
    """List all sessions for the logged-in user"""
    # Sessions where user is requester
    requested = Session.objects.filter(
        requester=request.user
    ).select_related('helper', 'helper__profile').order_by('-created_at')
    
    # Sessions where user is helper
    helping = Session.objects.filter(
        helper=request.user
    ).select_related('requester', 'requester__profile').order_by('-created_at')
    
    return render(request, 'exchanges/session_list.html', {
        'requested_sessions': requested,
        'helping_sessions': helping,
    })


@login_required
def session_detail_view(request, pk):
    """View details of a specific session"""
    session = get_object_or_404(Session, pk=pk)
    
    # Check if user is involved in this session
    is_involved = (request.user == session.requester or 
                   request.user == session.helper or 
                   request.user.is_staff)
    
    if not is_involved:
        messages.error(request, "You don't have permission to view this session.")
        return redirect('exchanges:list')
    
    return render(request, 'exchanges/session_detail.html', {
        'session': session,
    })


@login_required
def create_session_view(request):
    """Create a new exchange session"""
    if request.method == 'POST':
        helper_email = request.POST.get('helper_email', '').strip().lower()
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        duration = request.POST.get('duration', '60')
        level = request.POST.get('level', 'beginner')
        scheduled_time = request.POST.get('scheduled_time', '').strip()
        
        # Validation
        if not helper_email or not title:
            messages.error(request, "Please provide helper email and title.")
            return render(request, 'exchanges/create_session.html', {
                'suggested_helpers': User.objects.exclude(id=request.user.id).filter(email_verified=True)[:10],
                'helper_email': helper_email,
                'title': title,
                'description': description,
                'duration': duration,
                'level': level,
                'scheduled_time': scheduled_time,
            })
        
        try:
            # Find helper
            helper = User.objects.get(email__iexact=helper_email)
            
            # Check if not trying to help themselves
            if helper == request.user:
                messages.error(request, "You cannot create a session with yourself.")
                return render(request, 'exchanges/create_session.html', {
                    'suggested_helpers': User.objects.exclude(id=request.user.id).filter(email_verified=True)[:10],
                    'helper_email': helper_email,
                    'title': title,
                    'description': description,
                    'duration': duration,
                    'level': level,
                    'scheduled_time': scheduled_time,
                })
            
            # Create session (credits auto-calculated)
            session = Session(
                requester=request.user,
                helper=helper,
                title=title,
                description=description,
                duration=duration,
                level=level,
                status=Session.Status.PENDING
            )
            
            # Add scheduled time if provided
            if scheduled_time:
                from django.utils.dateparse import parse_datetime
                parsed_time = parse_datetime(scheduled_time)
                if parsed_time:
                    session.scheduled_time = parsed_time
            
            session.save()  # Credits auto-calculated in save()
            
            messages.success(request, f"Session created successfully! {session.agreed_amount} credits will be transferred upon completion.")
            return redirect('exchanges:detail', pk=session.pk)
            
        except User.DoesNotExist:
            messages.error(request, f"User with email '{helper_email}' not found.")
            return render(request, 'exchanges/create_session.html', {
                'suggested_helpers': User.objects.exclude(id=request.user.id).filter(email_verified=True)[:10],
                'helper_email': helper_email,
                'title': title,
                'description': description,
                'duration': duration,
                'level': level,
                'scheduled_time': scheduled_time,
            })
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'exchanges/create_session.html', {
                'suggested_helpers': User.objects.exclude(id=request.user.id).filter(email_verified=True)[:10],
                'helper_email': helper_email,
                'title': title,
                'description': description,
                'duration': duration,
                'level': level,
                'scheduled_time': scheduled_time,
            })
    
    # GET request - show form with suggested helpers
    suggested_helpers = User.objects.exclude(
        id=request.user.id
    ).filter(
        email_verified=True
    ).select_related('profile')[:10]
    
    # Pre-fill from query params
    helper_id = request.GET.get('helper', '')
    skill_id = request.GET.get('skill', '')
    
    helper_email = ''
    title = ''
    
    # Pre-fill helper email if helper provided
    # We support either a numeric user id (helper=12) or an email (helper=user@surrey.ac.uk)
    if helper_id:
        try:
            if str(helper_id).isdigit():
                helper_user = User.objects.get(id=int(helper_id))
            else:
                helper_user = User.objects.get(email__iexact=str(helper_id).strip())
            helper_email = helper_user.email
        except User.DoesNotExist:
            # If an invalid helper is provided, just render the page without prefilling.
            pass
    
    # Pre-fill title if skill_id provided
    if skill_id:
        try:
            from skills.models import Skill
            skill = Skill.objects.get(id=skill_id)
            title = f"Learn {skill.name}"
        except:
            pass
    
    return render(request, 'exchanges/create_session.html', {
        'suggested_helpers': suggested_helpers,
        'helper_email': helper_email,
        'pre_filled_title': title,
    })


@login_required
def accept_session_view(request, pk):
    """Accept a pending session (helper only)"""
    session = get_object_or_404(Session, pk=pk)
    
    # Check permissions
    if request.user != session.helper and not request.user.is_staff:
        messages.error(request, "Only the helper can accept this session.")
        return redirect('exchanges:detail', pk=pk)
    
    if session.status != Session.Status.PENDING:
        messages.info(request, f"Session is already {session.get_status_display()}.")
        return redirect('exchanges:detail', pk=pk)
    
    # Accept session
    session.status = Session.Status.ACCEPTED
    session.save(update_fields=['status', 'updated_at'])
    
    messages.success(request, "Session accepted! You can now provide help.")
    return redirect('exchanges:detail', pk=pk)


@login_required
def complete_session_view(request, pk):
    """Mark session as complete and transfer credits (requester only)"""
    session = get_object_or_404(Session, pk=pk)
    
    try:
        # This will check permissions and transfer credits
        session.mark_completed(by_user=request.user)
        messages.success(
            request, 
            f"Session completed! {session.agreed_amount} credits transferred to {session.helper.email}."
        )
    except ValidationError as e:
        messages.error(request, str(e))
    
    return redirect('exchanges:detail', pk=pk)


@login_required
def cancel_session_view(request, pk):
    """Cancel/decline a session (requester, helper, or admin)"""
    session = get_object_or_404(Session, pk=pk)
    
    # Check permissions - allow requester OR helper to cancel
    if request.user not in [session.requester, session.helper] and not request.user.is_staff:
        messages.error(request, "You don't have permission to cancel this session.")
        return redirect('exchanges:detail', pk=pk)
    
    if session.status == Session.Status.COMPLETED:
        messages.error(request, "Cannot cancel a completed session.")
        return redirect('exchanges:detail', pk=pk)
    
    if session.status == Session.Status.CANCELLED:
        messages.info(request, "Session is already cancelled.")
        return redirect('exchanges:detail', pk=pk)
    
    # Cancel session
    session.status = Session.Status.CANCELLED
    session.save(update_fields=['status', 'updated_at'])
    
    messages.success(request, "Session cancelled successfully.")
    return redirect('exchanges:detail', pk=pk)
