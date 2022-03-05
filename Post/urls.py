from django.urls import path, include
from .views import comment, like, posts, unlike, all_posts

urlpatterns = [
    path('posts/<int:pk>', posts.as_view()),
    path('posts/', posts.as_view()),
    path('like/<int:pk>', like),
    path('unlike/<int:pk>', unlike),
    path('comment/<int:pk>', comment),
    path('all_posts/', all_posts),
]
