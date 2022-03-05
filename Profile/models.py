from operator import imod, mod
from django.db import models
from Account.models import CustomUser


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    following = models.ManyToManyField(CustomUser, related_name="following")
    username = models.CharField(max_length=30, unique=True)
