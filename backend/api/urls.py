from django.urls import path

from . import views

urlpatterns = [
    path("posts", views.PostsView.as_view()),
    # path("posts", views.PostsEditView.as_view()),
]
