from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post


@api_view(["GET"])
def index(request):
    return Response({"message": "Welcome to Posts API"})


ITEMS = [
    {"id": 1, "title": "First item"},
    {"id": 2, "title": "Second item"},
]

@api_view(["GET"])
def hello_view(request):
    return Response({"message": "Hello from posts app"})

@api_view(["GET"])
def time_view(request):
    return Response({"now": datetime.now().isoformat()})

@api_view(["POST"])
def echo_view(request):
    return Response({"you_sent": request.data})

@api_view(["GET", "POST"])
def items_view(request):
    if request.method == "GET":
        return Response({"items": ITEMS})

    title = request.data.get("title")
    if not title:
        return Response({"error": "title is required"}, status=status.HTTP_400_BAD_REQUEST)

    new_id = max(i["id"] for i in ITEMS) + 1 if ITEMS else 1
    item = {"id": new_id, "title": title}
    ITEMS.append(item)
    return Response(item, status=status.HTTP_201_CREATED)


#def index(request):
    return HttpResponse("Hi! to see posts goo to /posts/")


class PostListAPIView(APIView):
    def get(self, request):
        posts = Post.objects.filter(
            is_published=True
        ).prefetch_related('authors__user')

        data = []

        for post in posts:
            authors = [
                {
                    "id": author.id,
                    "username": author.user.username,
                    "bio": author.bio
                }
                for author in post.authors.all()
            ]

            data.append({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "authors": authors,
                "is_published": post.is_published,
                "publish_date": post.publish_date.isoformat() if post.publish_date else None,
                "created_time": post.created_time.isoformat(),
                "modified_time": post.modified_time.isoformat()
            })

        return Response(data)



class AuthorListAPIView(APIView):
    def get(self, request):
        authors = Author.objects.all().prefetch_related('posts')

        data = []

        for author in authors:
            posts = [
                {
                    "id": post.id,
                    "title": post.title,
                    "publish_date": post.publish_date.isoformat() if post.publish_date else None
                }
                for post in author.posts.filter(is_published=True)
            ]

            data.append({
                "id": author.id,
                "username": author.user.username,
                "bio": author.bio,
                "posts": posts,
                "posts_count": len(posts)
            })

        return Response(data)



@api_view(["GET", "POST"])
def post_api_list_create(request):
    if request.method == "GET":
        posts = Post.objects.all()
        data = [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "authors": [a.user.username for a in post.authors.all()],
            }
            for post in posts
        ]
        return Response(data)

    elif request.method == "POST":
        title = request.data.get("title")
        content = request.data.get("content")
        author_ids = request.data.get("author_ids", [])

        if not title or not content:
            return Response(
                {"error": "title and content are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        post = Post.objects.create(title=title, content=content)

        if author_ids:
            authors = Author.objects.filter(id__in=author_ids)
            post.authors.set(authors)

        return Response(
            {
                "id": post.id,
                "title": post.title,
                "content": post.content
            },
            status=status.HTTP_201_CREATED
        )


@api_view(["GET", "PUT", "DELETE"])
def post_api_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(
            {"error": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "authors": [
                {"id": a.id, "username": a.user.username}
                for a in post.authors.all()
            ],
            "is_published": post.is_published,
        }
        return Response(data)

    elif request.method == "PUT":
        post.title = request.data.get("title", post.title)
        post.content = request.data.get("content", post.content)
        post.is_published = request.data.get("is_published", post.is_published)

        if "author_ids" in request.data:
            authors = Author.objects.filter(id__in=request.data["author_ids"])
            post.authors.set(authors)

        post.save()
        return Response({"message": "Post updated successfully"})

    elif request.method == "DELETE":
        post.delete()
        return Response(
            {"message": "Post deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

class PostListCreateAPIView(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)