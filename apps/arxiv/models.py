from django.contrib.auth import get_user_model
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    user_starts = models.ManyToManyField(get_user_model(), blank=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    remote_id = models.CharField(unique=True, max_length=100)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    authors = models.ManyToManyField(Author)
    published = models.DateTimeField()

    user_starts = models.ManyToManyField(get_user_model(), blank=True)

    def __str__(self):
        return self.title
