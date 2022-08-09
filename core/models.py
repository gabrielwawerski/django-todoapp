from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from core import config


class List(models.Model):
    list_name = models.CharField(max_length=config.LIST_NAME_MAX_LENGTH)
    date_created = models.DateTimeField('date created', auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    contributors = models.ManyToManyField(User)

    def __str__(self):
        return self.list_name

    def get_absolute_url(self):
        return f'/{self.list_name}/'


class ListEntry(models.Model):
    list = models.ForeignKey(List, related_name='entries', on_delete=models.CASCADE)
    entry_text = models.CharField(max_length=config.ENTRY_TEXT_MAX_LENGTH)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.entry_text
