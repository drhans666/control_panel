from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Anon(models.Model):
    title = models.CharField(max_length=200, default='')
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.title[:50] + '...'

