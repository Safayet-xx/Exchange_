from django.urls import path
from .views import home_view
from .search_views import unified_search_view

app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    path("search/", unified_search_view, name="search"),
]
