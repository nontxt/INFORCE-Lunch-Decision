from . import accounts_load, menu_load, restaurant_load, votes_load, create_admin, group_load


def run():
    """
    Pre-population script
    """
    print('Pre-populating')
    group_load.run()
    accounts_load.run()
    restaurant_load.run()
    menu_load.run()
    votes_load.run()
    create_admin.run()
    print('Done')
