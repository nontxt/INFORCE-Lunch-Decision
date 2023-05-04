from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey('account.Owner', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class DailyMenu(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='menu')
    items = models.TextField()
    customers_vote = models.ManyToManyField('account.Employee', related_name='votes')

    def __str__(self):
        return f"{self.restaurant.name}'s menu"

