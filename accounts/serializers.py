from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'content', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']
