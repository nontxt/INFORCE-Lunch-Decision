from django.test import TestCase
from django.contrib.auth import get_user_model

from faker import Faker

from lunch.models import Restaurant, DailyMenu
from account.models import Employee, Owner

user_model = get_user_model()
fake = Faker()


class Setup(TestCase):

    def setUp(self):
        owner = user_model.objects.create_user(username=fake.simple_profile()['username'],
                                               email=fake.email(),
                                               password=fake.password(),
                                               first_name=fake.first_name(),
                                               last_name=fake.last_name()
                                               )
        self.owner = Owner.objects.create(user=owner)


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


class DailyMenuModelTestCase(Setup):

    def setUp(self):
        super().setUp()
        self.restaurant1 = Restaurant.objects.create(name="LittleLemon", address='8 Union st.', owner=self.owner)
        self.restaurant2 = Restaurant.objects.create(name="Dominos", address='100 Heroes st.', owner=self.owner)

        customer = user_model.objects.create_user(username=fake.simple_profile()['username'],
                                                  email=fake.email(),
                                                  password=fake.password(),
                                                  first_name=fake.first_name(),
                                                  last_name=fake.last_name()
                                                  )
        self.customer1 = Employee.objects.create(user=customer)

        customer = user_model.objects.create_user(username=fake.simple_profile()['username'],
                                                  email=fake.email(),
                                                  password=fake.password(),
                                                  first_name=fake.first_name(),
                                                  last_name=fake.last_name()
                                                  )
        self.customer2 = Employee.objects.create(user=customer)

        self.items = """
        1. Pizza
        2. Pasta
        3. Desert
        4. Cake
        """

        self.menu = DailyMenu.objects.create(restaurant=self.restaurant1, items=self.items)

    def test_create(self):
        """
        Test creating a menu
        """

        menu = DailyMenu.objects.create(restaurant=self.restaurant2, items=self.items)

        self.assertEqual(menu.id, 2)
        self.assertEqual(menu.restaurant, self.restaurant2)

    def test_delete(self):
        """
        Test deleting a menu
        """

        self.assertEqual(self.menu.id, 1)
        self.menu.delete()
        with self.assertRaises(DailyMenu.DoesNotExist):
            DailyMenu.objects.get(id=1)

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
