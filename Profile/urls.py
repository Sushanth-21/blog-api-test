from django.urls import path, include
from .views import profile_setup, follow, unfollow, user

urlpatterns = [
    path('profile_setup/', profile_setup),
    path('follow/<int:pk>', follow),
    path('unfollow/<int:pk>', unfollow),
    path('user', user),
]
