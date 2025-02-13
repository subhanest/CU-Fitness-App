from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    receive_updates = models.BooleanField(default=False)

    def __str__(self):
        return self.username
