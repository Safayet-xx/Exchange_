from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('create/', views.post_create, name='create'),
    path('my/', views.my_posts, name='my_posts'),
    path('<int:pk>/', views.post_detail, name='detail'),
    path('<int:pk>/delete/', views.post_delete, name='delete'),
]
