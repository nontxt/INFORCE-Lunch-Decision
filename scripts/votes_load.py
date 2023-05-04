from random import choice

from lunch.models import DailyMenu
from account.models import Employee


def run():
    menus = DailyMenu.objects.all()

    for menu in menus:
        menu.customers_vote.clear()

    for customer in Employee.objects.all():
        menu = choice(menus)
        menu.customers_vote.add(customer)
