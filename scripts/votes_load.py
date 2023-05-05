from random import choice

from django.contrib.auth.models import User

from lunch.models import Menu


def run():
    """
    Pre-populate votes
    """
    menus = Menu.objects.all()

    for menu in menus:
        menu.customers_vote.clear()

    for customer in User.objects.filter(groups__name='Employee'):
        menu = choice(menus)
        menu.customers_vote.add(customer)
