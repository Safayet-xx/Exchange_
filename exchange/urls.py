"""
Main URL Configuration for Exchange Platform
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from profiles.views import public_profile_view, user_search_view

urlpatterns = [
    # Admin panel (can be customized for security)
    path(settings.ADMIN_URL, admin.site.urls),

    # Core/Home
    path("", include(("core.urls", "core"), namespace="core")),

    # Authentication
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),

    # Profile Management
    path("profiles/", include(("profiles.urls", "profiles"), namespace="profiles")),

    # Credits & Wallet
    path("credits/", include(("credits.urls", "credits"), namespace="credits")),

    # Posts - Marketplace for offering/requesting help
    path("posts/", include(("posts.urls", "posts"), namespace="posts")),

    # Skills - Profile skills (user expertise)
    path("skills/", include(("skills.urls", "skills"), namespace="skills")),

    # Exchanges/Sessions
    path("exchanges/", include(("exchanges.urls", "exchanges"), namespace="exchanges")),

    # Public User Profiles & Search
    path("u/<str:handle>/", public_profile_view, name="public_profile"),
    path("search/", user_search_view, name="user_search"),

    # REST API (future)
    # path("api/", include("api.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site configuration
admin.site.site_header = "Exchange Platform Admin"
admin.site.site_title = "Exchange Admin"
admin.site.index_title = "Welcome to Exchange Admin Panel"
