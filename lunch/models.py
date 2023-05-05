from django.db import models
from django.conf import settings


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu')
    items = models.TextField()
    date = models.DateField(auto_now_add=True)
    customers_vote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='votes')

    class Meta:
        unique_together = ["restaurant", "date"]  # Owner can add only one menu per day

    def __str__(self):
        return f"{self.restaurant.name}'s menu"
