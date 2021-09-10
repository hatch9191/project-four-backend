from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Post, Comment
from .serializers import (
    CommentSerializer,
    PostSerializer,
    PostDetailSerializer,
    BasicPostSerializer
)


class PostListView(APIView):
    # show all posts and create a post
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        posts = Post.objects.all()
        serialized_post = PostSerializer(posts, many=True)
        return Response(serialized_post.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['owner'] = request.user.id
        post_to_create = BasicPostSerializer(data=request.data)
        if post_to_create.is_valid():
            post_to_create.save()
            return Response(post_to_create.data, status=status.HTTP_201_CREATED)
        return Response(post_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    # show/delete/edit a post

    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class CommentListView(APIView):
    # create a comment on a post
    permission_classes = (IsAuthenticated, )

    def post(self, request, post_pk):
        request.data['post'] = post_pk
        request.data['owner'] = request.user.id
        created_comment = CommentSerializer(data=request.data)
        if created_comment.is_valid():
            created_comment.save()
            return Response(created_comment.data, status=status.HTTP_201_CREATED)
        return Response(created_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CommentDetailView(APIView):
    # delete a comment on a post
    permission_classes = (IsAuthenticated, )

    def delete(self, _request, **kwargs):
        comment_pk = kwargs['comment_pk']
        try:
            comment_to_delete = Comment.objects.get(pk=comment_pk)
            comment_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise NotFound(detail='Comment not found')


class PostSaveView(APIView):
    # user saves a post 
    permission_classes = (IsAuthenticated, )

    def post(self, request, post_pk):
        try:
            post_to_save = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise NotFound()
        if request.user in post_to_save.saved_by.all():
            post_to_save.saved_by.remove(request.user.id)
        else:
            post_to_save.saved_by.add(request.user.id)
        serialized_post = PostSerializer(post_to_save)
        return Response(serialized_post.data, status=status.HTTP_202_ACCEPTED)
