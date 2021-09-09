from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    CommentListView,
    CommentDetailView,
    PostSaveView
)


urlpatterns = [
    path('', PostListView.as_view()),
    path('<int:pk>/', PostDetailView.as_view()),
    path('<int:post_pk>/comments/', CommentListView.as_view()),
    path('<int:post_pk>/comments/<int:comment_pk>/', CommentDetailView.as_view()),
    path('<int:post_pk>/save/', PostSaveView.as_view())
]
