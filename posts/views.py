from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post
from .serializers import PostSerializer, PostDetailSerializer


class PostListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        posts = Post.objects.all()
        serialized_post = PostSerializer(posts, many=True)
        return Response(serialized_post.data, status=status.HTTP_200_OK)

    def post(self, request):

        post_to_create = PostSerializer(data=request.data)
        if post_to_create.is_valid():
            post_to_create.save()
            return Response(post_to_create.data, status=status.HTTP_200_OK)
        return Response(post_to_create.data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    '''Detail view for /posts/id SHOW/ UPDATE/ DELETE'''

    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
