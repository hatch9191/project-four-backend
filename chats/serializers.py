from django.core.checks import messages
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Chat, Message

User = get_user_model()


# class ChatSerializer(serializers.ModelSerializer):

#     class Meta:
#         model: Chat
#         fields = '__all__'

class NestedMessageUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'profile_image')


class MessageSerializer(serializers.ModelSerializer):
    # sender = NestedMessageUserSerializer()
    # recipient = NestedMessageUserSerializer()

    class Meta:
        model = Message
        fields = '__all__'


class PopulateMessageSerializer(MessageSerializer):
    sender = NestedMessageUserSerializer()
    recipient = NestedMessageUserSerializer()


class BasicChatSerializer(serializers.ModelSerializer):
    messages = PopulateMessageSerializer(many=True)
    user_a = NestedMessageUserSerializer()
    user_b = NestedMessageUserSerializer()

    class Meta:
        model = Chat
        fields = ('id', 'user_a', 'user_b', 'messages')


class CreateChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('id', 'user_a', 'user_b')
