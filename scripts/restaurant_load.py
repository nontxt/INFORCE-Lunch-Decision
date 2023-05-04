from faker import Faker

from lunch.models import Restaurant
from account.models import Owner


def run():
    names = [
        'The Rusty Spoon',
        'La Petite Boulangerie',
        'The Blue Plate',
        'Saffron Indian Cuisine',
        'The Burger Joint',
        'The Cheesy Tomato',
        'Tokyo Grill & Sushi Bar',
        'The Green Leaf Café',
        'The Rustic Table',
        'The Corner Bistro',
    ]
    fake = Faker()
    Restaurant.objects.all().delete()

    for owner in Owner.objects.all():
        Restaurant.objects.create(name=names.pop(), address=fake.address(), owner=owner)
