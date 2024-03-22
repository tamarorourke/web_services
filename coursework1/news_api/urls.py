from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("stories/post", views.post_story, name="post_story"),
    path("stories/", views.stories, name="stories"),
    path("stories/<int:story_id>/", views.delete_story, name="delete_story")  
]