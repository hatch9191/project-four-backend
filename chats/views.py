from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Chat, Message
from .serializers import BasicChatSerializer, MessageSerializer, CreateChatSerializer, PopulateMessageSerializer
from django.db.models import Q


class ChatListAllUserView(APIView):

    # filtered chats to get all chats that the user is in
    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        sender = request.user.id

        chats_of_user = Chat.objects.filter(
            (Q(user_a=sender) | Q(user_b=sender)))
        serialized_chat_of_user = BasicChatSerializer(chats_of_user, many=True)
        return Response(serialized_chat_of_user.data, status=status.HTTP_200_OK)


# class ChatListView(APIView):

#     # filtered chats to find chat of user and profile the user is on
#     permission_classes = (IsAuthenticated, )

#     def get(self, request, profile_pk):
#         sender = request.user.id
#         recipient = profile_pk

#         chats = Chat.objects.filter((Q(user_a=sender) & Q(user_b=recipient)) | (
#             Q(user_b=sender) & Q(user_a=recipient)))

#         serialized_chat = CreateChatSerializer(chats, many=True)
#         return Response(serialized_chat.data, status=status.HTTP_200_OK)


class ChatListView(APIView):
    # filtered chats to find chat of user and profile the user is on

    permission_classes = (IsAuthenticated, )

    def get(self, request, profile_pk):
        sender = request.user.id
        recipient = profile_pk
        chats = Chat.objects.filter(
            (Q(user_a=sender) & Q(user_b=recipient)) |
            (Q(user_b=sender) & Q(user_a=recipient)))
        serialized_chat = CreateChatSerializer(chats, many=True)
        if len(chats) < 1:
            raise NotFound(detail='Chat not found')
        else:
            return Response(serialized_chat.data, status=status.HTTP_200_OK)
        # except Chat.DoesNotExist:
        #     raise NotFound(detail='Chat not found')


class ChatCreateView(APIView):

    # create a chat
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        request.data['user_a'] = request.user.id
        request.data['user_b'] = pk

        created_chat = CreateChatSerializer(data=request.data)
        if created_chat.is_valid():
            created_chat.save()
            return Response(created_chat.data, status=status.HTTP_201_CREATED)
        return Response(created_chat.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SingleChatView(APIView):

    def get(self, _request, profile_pk, chat_pk):
        try:
            placeholder = profile_pk
            chat_to_show = Chat.objects.get(id=chat_pk)
        except Chat.DoesNotExist:
            raise NotFound()
        serialized_chat = BasicChatSerializer(chat_to_show)
        return Response(serialized_chat.data, status=status.HTTP_200_OK)


class MessageListView(APIView):

    permission_classes = (IsAuthenticated, )

    # get all messages for a user
    def get(self, request, **kwargs):
        id_of_user = request.user.id
        messages_to_get = Message.objects.filter(
            (Q(sender=id_of_user) | Q(recipient=id_of_user)))
        serialized_message = MessageSerializer(messages_to_get, many=True)
        return Response(serialized_message.data, status=status.HTTP_200_OK)

    # create a message

    def post(self, request, **kwargs):
        request.data['chat'] = kwargs['chat_pk']
        request.data['sender'] = request.user.id
        request.data['recipient'] = kwargs['profile_pk']

        created_message = MessageSerializer(data=request.data)
        if created_message.is_valid():
            created_message.save()
            return Response(created_message.data, status=status.HTTP_201_CREATED)
        return Response(created_message.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class MessageDetailVeiw(APIView):

    # Delete a message
    permission_classes = (IsAuthenticated, )

    def delete(self, _request, **kwargs):
        message_pk = kwargs['message_pk']
        try:
            message_to_delete = Message.objects.get(pk=message_pk)
            message_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            raise NotFound(detail='Message not found')
