from django.db import models
from django.db.models.deletion import CASCADE
# from django.db.models.fields import related


class Chat(models.Model):
    user_a = models.ForeignKey(
        'jwt_auth.User',
        related_name='chats_a',
        on_delete=models.CASCADE
    )
    user_b = models.ForeignKey(
        'jwt_auth.User',
        related_name='chats_b',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.id}'


class Message(models.Model):
    content = models.TextField(max_length=350)
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(
        Chat,
        related_name='messages',
        on_delete=CASCADE
    )
    sender = models.ForeignKey(
        'jwt_auth.User',
        related_name='messages_sent',
        on_delete=CASCADE
    )
    recipient = models.ForeignKey(
        'jwt_auth.User',
        related_name='messages_received',
        on_delete=CASCADE
    )
