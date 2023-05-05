from random import choices

from lunch.models import Restaurant, Menu

deserts = [
    'Apple pie',
    'Pumpkin pie',
    'Banana split',
    'Giant chocolate chip cookies',
    'Molten lava cakes',
    'Cinnamon rolls',
    'Cheesecake',
    'Baklava',
    'Lemon cake',
    'Cannoli',
    'Strawberry shortcake',
    'Apple Cobbler'
]

appetizers = [
    'Mozzarella sticks',
    'Cheddar Biscuits',
    'Mac & cheese',
    'Pigs in a blanket',
    'Spinach cheese dip with chips',
    'Onion rings',
    'French fries',
    'Baked potato',
    'Breadsticks',
    'Salad',
]
main = [
    'Chicken pot pie',
    'Mashed potatoes',
    'Fried chicken',
    'Burgers',
    'Chicken soup',
    'Meatloaf',
    'Lasagna',
    'Spaghetti with meatballs',
    'Chicken burger',
    'Chicken parmesan',
    'Chicken Pesto',
    'Burger Sliders'
]


def run():
    """
    Pre-populate menus for restaurants
    """
    Menu.objects.all().delete()

    for restaurant in Restaurant.objects.all():
        menu = []
        for meal_type in [main, appetizers, deserts]:
            while True:
                items = choices(meal_type, k=2)
                if len(items) == 2:
                    menu.extend(items)
                    break
        Menu.objects.create(restaurant=restaurant, items='\n'.join(menu))
