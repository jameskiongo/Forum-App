from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Posts
from .serializers import PostSerializer

# from rest_framework.response import Response


# Create your views here.


# ╭──────────────────────────────────────────────────────────╮
# │ Post view                                                │
# ╰──────────────────────────────────────────────────────────╯


class PostsView(generics.ListCreateAPIView):
    """Add posts"""

    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    # permission_classes = [IsAuthenticated]
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
