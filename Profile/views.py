from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from Account.models import CustomUser
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_setup(request):
    try:
        profile, t = Profile.objects.get_or_create(user=request.user)
        profile.username = request.data.get("username")
        profile.save()
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': ProfileSerializer(profile).data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, pk):
    try:
        profile, t = Profile.objects.get_or_create(user=request.user)
        user = CustomUser.objects.get(id=int(pk))
        profile.following.add(user)
        profile.save()
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': ProfileSerializer(profile).data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow(request, pk):
    try:
        profile, t = Profile.objects.get_or_create(user=request.user)
        user = CustomUser.objects.get(id=int(pk))
        profile.following.remove(user)
        profile.save()
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': ProfileSerializer(profile).data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request):
    try:
        profile = Profile.objects.get(user=request.user)
        following = len(profile.following.all())
        followers = len(Profile.objects.filter(following=request.user))
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'username': profile.username, "followers": followers, "following": following})
