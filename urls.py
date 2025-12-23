from django.urls import path
from . import views

app_name = "exchanges"

urlpatterns = [
    # List and create
    path("", views.session_list_view, name="list"),
    path("create/", views.create_session_view, name="create"),
    
    # Session detail and actions
    path("<int:pk>/", views.session_detail_view, name="detail"),
    path("<int:pk>/accept/", views.accept_session_view, name="accept"),
    path("<int:pk>/complete/", views.complete_session_view, name="complete"),
    path("<int:pk>/cancel/", views.cancel_session_view, name="cancel"),
]
