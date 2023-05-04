from . import accounts_load, menu_load, restaurant_load, votes_load


def run():
    accounts_load.run()
    restaurant_load.run()
    menu_load.run()
    votes_load.run()
