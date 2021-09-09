from django.urls import path
from .views import (
    PostListView,
    PostDetailView
)


urlpatterns = [
    path('', PostListView.as_view()),
    path('<int:posts_pk>/', PostDetailView.as_view())
]
