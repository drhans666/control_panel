from django.db import models
from django.contrib.auth.models import User
from inventory.models import Section


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    section = models.ManyToManyField(Section)

    def __str__(self):
        return self.user.username
