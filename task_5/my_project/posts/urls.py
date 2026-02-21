from django.urls import path
from . import views
from django.urls import path
from .views import (
    index,
    PostListAPIView,
    AuthorListAPIView,
)
from .views import PostListCreateAPIView

urlpatterns = [
    path("", index),
    path("posts/", PostListAPIView.as_view()),
    path("authors/", AuthorListAPIView.as_view()),
    path('posts/', PostListCreateAPIView.as_view()),
    path("", views.index, name="index"),  # /posts/

    # ---- Utility endpoints ----
    path("hello/", views.hello_view, name="hello"),  # /posts/hello/
    path("time/", views.time_view, name="time"),     # /posts/time/
    path("echo/", views.echo_view, name="echo"),     # /posts/echo/
    path("items/", views.items_view, name="items"),  # /posts/items/

    # ---- API endpoints ----
    path("list/", views.PostListAPIView.as_view(), name="posts-list"),      # /posts/list/
    path("authors-list/", views.AuthorListAPIView.as_view(), name="authors-list"),  # /posts/authors-list/

    # ---- CRUD for posts ----
    path("api/", views.post_api_list_create, name="posts-api"),            # GET/POST /posts/api/
    path("api/<int:pk>/", views.post_api_detail, name="posts-api-detail"), # GET/PUT/DELETE /posts/api/1/
]

