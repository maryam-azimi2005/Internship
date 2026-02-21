from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Post, Comment


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'username', 'bio']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'text', 'created_time']

class PostSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'authors',
            'is_published',
            'publish_date',
            'created_time',
            'modified_time',
            'comments'
        ]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long."
            )
        return value

    def validate(self, data):
        if data.get('is_published') and not data.get('publish_date'):
            raise serializers.ValidationError(
                "Published posts must have a publish date."
            )
        return data