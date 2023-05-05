from django.test import TestCase
from django.contrib.auth.models import User, Group
from faker import Faker

from lunch.models import Restaurant, Menu

fake = Faker()


class Setup(TestCase):

    def setUp(self):
        owner_group, _ = Group.objects.get_or_create(name='Owner')
        self.owner = User.objects.create_user(username=fake.simple_profile()['username'],
                                              email=fake.email(),
                                              password=fake.password(),
                                              first_name=fake.first_name(),
                                              last_name=fake.last_name()
                                              )
        owner_group.user_set.add(self.owner)


class RestaurantModelTestCase(Setup):

    def test_create(self):
        """
        Test creating a restaurant
        """
        restaurant = Restaurant.objects.create(name="LittleLemon", address='8 Union st.', owner=self.owner)
        self.assertEqual(restaurant.id, 1)
        self.assertEqual(restaurant.owner, self.owner)
        self.assertEqual(restaurant.name, "LittleLemon")

    def test_ordering(self):
        """
        Test ordering
        """
        Restaurant.objects.create(name="ZYX", address="zyx", owner=self.owner)
        Restaurant.objects.create(name="ABC", address="abc", owner=self.owner)
        restaurants = Restaurant.objects.values_list('id', 'name')

        self.assertEqual(restaurants[0][0], 2)
        self.assertEqual(restaurants[0][1], 'ABC')

    def test_delete(self):
        """
        Test deleting a restaurant
        """
        restaurant = Restaurant.objects.create(name="LittleLemon", address='8 Union st.', owner=self.owner)

        self.assertEqual(restaurant.id, 1)
        restaurant.delete()
        with self.assertRaises(Restaurant.DoesNotExist):
            Restaurant.objects.get(id=1)


class MenuModelTestCase(Setup):

    def setUp(self):
        super().setUp()
        self.restaurant1 = Restaurant.objects.create(name="LittleLemon", address='8 Union st.', owner=self.owner)
        self.restaurant2 = Restaurant.objects.create(name="Dominos", address='100 Heroes st.', owner=self.owner)

        employee_group, _ = Group.objects.get_or_create(name='Employee')
        self.customer1 = User.objects.create_user(username=fake.simple_profile()['username'],
                                                  email=fake.email(),
                                                  password=fake.password(),
                                                  first_name=fake.first_name(),
                                                  last_name=fake.last_name()
                                                  )

        self.customer2 = User.objects.create_user(username=fake.simple_profile()['username'],
                                                  email=fake.email(),
                                                  password=fake.password(),
                                                  first_name=fake.first_name(),
                                                  last_name=fake.last_name()
                                                  )
        employee_group.user_set.set([self.customer1, self.customer2])

        self.items = """
        1. Pizza
        2. Pasta
        3. Desert
        4. Cake
        """

        self.menu = Menu.objects.create(restaurant=self.restaurant1, items=self.items)

    def test_create(self):
        """
        Test creating a menu
        """

        menu = Menu.objects.create(restaurant=self.restaurant2, items=self.items)

        self.assertEqual(menu.id, 2)
        self.assertEqual(menu.restaurant, self.restaurant2)

    def test_delete(self):
        """
        Test deleting a menu
        """

        self.assertEqual(self.menu.id, 1)
        self.menu.delete()
        with self.assertRaises(Menu.DoesNotExist):
            Menu.objects.get(id=1)

    def test_votes(self):
        """
        Test setting a votes
        """

        self.assertEqual(self.menu.customers_vote.count(), 0)
        self.menu.customers_vote.set([self.customer1, self.customer2])
        self.assertEqual(self.menu.customers_vote.count(), 2)

    def test_remove_votes(self):
        """
        Test removing a votes
        """
        self.menu.customers_vote.set([self.customer1, self.customer2])
        self.assertEqual(self.menu.customers_vote.count(), 2)
        self.menu.customers_vote.remove(self.customer1)
        self.assertEqual(self.menu.customers_vote.count(), 1)

    def test_cleat_votes(self):
        """
        Test removing an all votes
        """
        self.menu.customers_vote.set([self.customer1, self.customer2])
        self.assertEqual(self.menu.customers_vote.count(), 2)
        self.menu.customers_vote.clear()
        self.assertEqual(self.menu.customers_vote.count(), 0)
