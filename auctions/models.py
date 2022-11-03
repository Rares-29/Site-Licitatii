from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING


class User(AbstractUser):
    location = models.CharField(max_length = 200)
    def __str__(self):
        user = self.get_username()
        return user


class Category(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return (f"{self.name}")

class Item(models.Model):
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 1000)
    Image = models.ImageField(upload_to="images/")
    price = models.FloatField()
    seller = models.CharField(max_length = 100)
    winner = models.CharField(max_length = 100, null = True, blank = True)
    category = models.ForeignKey(Category, on_delete = CASCADE, related_name = "Item_cat")
    date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return (f"{self.name}")

class Bid(models.Model):
    bidder = models.CharField(max_length = 100, blank = True)
    offer = models.FloatField()
    Name = models.CharField(max_length = 100, blank = True)
    Number = models.CharField(max_length = 15, blank  = True)
    item = models.OneToOneField(Item, on_delete = CASCADE, related_name = "bid")
    peoples = models.IntegerField()

class Watchlist(models.Model):
    user = models.CharField(max_length = 100)
    product = models.ManyToManyField(Item, related_name = "watchlist", blank = True)
    def __str__(self):
        return (f"{self.user}")

class Comment(models.Model):
    user_com = models.CharField(max_length = 100)
    comment = models.CharField(max_length = 1000)
    product_id = models.ForeignKey(Item, on_delete = CASCADE, related_name = "comments")
    date = models.DateTimeField(auto_now_add = True)
