from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import Profile
from Account.serializers import UserSerializer


class ProfileSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
