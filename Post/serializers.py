from dataclasses import field
from venv import create
from rest_framework.serializers import ModelSerializer
from .models import Post
from Profile.serializers import ProfileSerializer


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'created_time')
