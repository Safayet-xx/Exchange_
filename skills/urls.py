from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.my_skills, name='my_skills'),
    path('add/', views.add_skill, name='add'),
    path('browse/', views.browse_skills, name='browse'),
    path('<int:pk>/edit/', views.edit_skill, name='edit'),
    path('<int:pk>/delete/', views.delete_skill, name='delete'),
]
