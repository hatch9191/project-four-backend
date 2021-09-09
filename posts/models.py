from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=250)
    image = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'
