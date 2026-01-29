from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post-list'),
    path('authors/', views.author_list, name='author-list'),
]

