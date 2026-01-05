"""
Stytch Authentication Helper
Handles magic link authentication with Stytch
"""
import stytch
from django.conf import settings


class StytchClient:
    """Singleton Stytch client"""
    _client = None
    
    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = stytch.Client(
                project_id=settings.STYTCH_PROJECT_ID,
                secret=settings.STYTCH_SECRET,
                environment=settings.STYTCH_ENVIRONMENT,
            )
        return cls._client


def send_magic_link(email, redirect_url=None):
    """
    Send magic link to user's email
    
    Args:
        email: User's email address
        redirect_url: Where to redirect after authentication
        
    Returns:
        dict: Response from Stytch API
    """
    client = StytchClient.get_client()
    
    try:
        response = client.magic_links.email.send(
            email=email,
            login_magic_link_url=redirect_url or f"{settings.STYTCH_PROJECT_DOMAIN}/authenticate",
            signup_magic_link_url=redirect_url or f"{settings.STYTCH_PROJECT_DOMAIN}/authenticate",
        )
        return {
            'success': True,
            'request_id': response.request_id,
            'user_id': response.user_id,
            'email_id': response.email_id,
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def authenticate_magic_link(token):
    """
    Authenticate a magic link token
    
    Args:
        token: Magic link token from URL
        
    Returns:
        dict: User information if successful
    """
    client = StytchClient.get_client()
    
    try:
        response = client.magic_links.authenticate(
            token=token,
            session_duration_minutes=60 * 24 * 7,  # 7 days
        )
        
        return {
            'success': True,
            'user_id': response.user_id,
            'email': response.user.emails[0].email if response.user.emails else None,
            'session_token': response.session_token,
            'session_jwt': response.session_jwt,
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def verify_session(session_token):
    """
    Verify an active session
    
    Args:
        session_token: Session token to verify
        
    Returns:
        dict: Session information if valid
    """
    client = StytchClient.get_client()
    
    try:
        response = client.sessions.authenticate(
            session_token=session_token
        )
        
        return {
            'success': True,
            'user_id': response.user_id,
            'session': response.session,
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def revoke_session(session_token):
    """
    Revoke/logout a session
    
    Args:
        session_token: Session token to revoke
        
    Returns:
        bool: True if successful
    """
    client = StytchClient.get_client()
    
    try:
        client.sessions.revoke(session_token=session_token)
        return True
    except Exception:
        return False
