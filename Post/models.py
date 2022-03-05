from statistics import mode
from django.db import models
from Account.models import CustomUser
from Profile.models import Profile


class Post(models.Model):
    created_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="created_by")
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_time = models.TimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
