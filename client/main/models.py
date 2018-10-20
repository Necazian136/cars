from django.db import models


class User(models.Model):
    login = models.CharField(max_length=63)
    password = models.CharField(max_length=63)
    token = models.CharField(max_length=63, default=None, null=True)


class Plate(models.Model):
    number = models.CharField(max_length=15)
    user_id = models.IntegerField()


class Synchronization(models.Model):
    request = models.CharField(max_length=1024)
    user_id = models.CharField(max_length=63, default=None, null=True)