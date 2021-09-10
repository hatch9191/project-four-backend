from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=250)
    image = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    saved_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='saved_posts',
        blank=True
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='created_posts',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    text = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='comments_made',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.post} - {self.id}'
