from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "date_posted",
            "author",
            "author_username",
        )
        read_only_fields = ("id", "date_posted", "author", "author_username")
