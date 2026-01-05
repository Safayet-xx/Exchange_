from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("setup/", views.profile_setup_view, name="setup"),
    path("search/", views.user_search_view, name="user_search"),
    path("@<str:handle>/", views.public_profile_view, name="public_profile"),
]
