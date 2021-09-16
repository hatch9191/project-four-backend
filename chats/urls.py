from django.urls import path
from .views import (
    ChatListView,
    ChatListAllUserView,
    ChatCreateView,
    SingleChatView,
    MessageListView,
    MessageDetailVeiw,
    MessageEditView
)

urlpatterns = [
    path('profile/<int:profile_pk>/chats/<int:chat_pk>/',
         SingleChatView.as_view()),
    path('profile/<int:profile_pk>/loadchats/',
         ChatListView.as_view()),
    path('profile/<int:profile_pk>/loaduserchats/',
         ChatListAllUserView.as_view()),
    path('profile/<int:pk>/chats/',
         ChatCreateView.as_view()),
    path('profile/<int:profile_pk>/chats/<int:chat_pk>/messages/',
         MessageListView.as_view()),
    path('profile/<int:profile_pk>/chats/<int:chat_pk>/messages/<int:message_pk>/',
         MessageDetailVeiw.as_view()),
    path('profile/<int:profile_pk>/chats/<int:chat_pk>/messages/<int:message_pk>/edit/',
         MessageEditView.as_view())
]
