from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255) # username
    email = models.EmailField(unique=True) # email
    phone = models.CharField(max_length=15, blank=True, null=True) # phone number (optional)
    age = models.PositiveIntegerField(blank=True, null=True) # age of user (optional)
    gender = models.CharField(max_length=10, blank=True, null=True) # gender of user (optional)

    def __str__(self):
        return self.name