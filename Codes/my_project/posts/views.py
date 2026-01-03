from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from rest_framework.response import Response


# Create your views here.

def index(request):
    #body
    return HttpResponse("Hello, world.")

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
