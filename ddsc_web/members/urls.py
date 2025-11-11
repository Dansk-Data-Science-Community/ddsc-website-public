from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = "members"


urlpatterns = [
    path("register/", views.RegisterMember.as_view(), name="register_member"),
    path("edit/", views.edit_member, name="edit"),
    path("unsubscribe/", views.unsubscribe, name="unsubscribe"),
    path("board/", views.board_members, name="board"),
    path("articles/", views.articles, name="articles"),
    path("salary", views.salary, name="salary"),
]
