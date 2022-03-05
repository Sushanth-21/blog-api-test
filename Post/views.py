from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from Account.models import CustomUser
from rest_framework import status
from .models import Post, Comment
from Profile.models import Profile
from .serializers import PostSerializer
from rest_framework.views import APIView


class posts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=int(pk))
            likes = len(post.likes.all())
            comments = len(Comment.objects.filter(post=post))
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"id": pk, "title": post.title, "description": post.description, "likes": likes, "comments": comments})

    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            post = Post.objects.create(
                title=request.data['title'], description=request.data['description'], created_by=profile)
            data = PostSerializer(post).data
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=int(pk))
            profile = Profile.objects.get(user=request.user)
            if profile == post.created_by:
                post.delete()
            else:
                return Response({"error": "user is not authorized to perform delete operation on post with id - {}".format(pk)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "deleted post with id - {}".format(pk)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request, pk):
    try:
        post = Post.objects.get(id=int(pk))
        profile = Profile.objects.get(user=request.user)
        post.likes.add(profile)
        post.save()
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "success"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike(request, pk):
    try:
        post = Post.objects.get(id=int(pk))
        profile = Profile.objects.get(user=request.user)
        post.likes.remove(profile)
        post.save()
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "success"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request, pk):
    try:
        post = Post.objects.get(id=int(pk))
        profile = Profile.objects.get(user=request.user)
        comment = Comment.objects.create(
            comment=request.data['comment'], user=profile, post=post)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"comment_id": comment.id})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_posts(request):
    try:
        data = []
        posts = Post.objects.all()
        posts = sorted(posts, key=lambda p: p.created_time)
        for p in posts:
            d = PostSerializer(p).data
            cmnts = Comment.objects.filter(post=p)
            arr = []
            for c in cmnts:
                arr.append(c.comment)
            d['comments'] = arr
            d['likes'] = len(p.likes.all())
            data.append(d)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(data)
