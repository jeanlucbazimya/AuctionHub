from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    pass
class Listings(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    start = models.FloatField(max_length=10)
    category = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.FileField(upload_to='',blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    status = models.CharField(default="open", max_length=60)
    watched = models.CharField(default="no", max_length=10)
class Bids(models.Model):
    amount = models.FloatField(max_length=10)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
class Comment(models.Model):
    comment = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

class Watch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    watched = models.CharField(default="yes", max_length=10)
