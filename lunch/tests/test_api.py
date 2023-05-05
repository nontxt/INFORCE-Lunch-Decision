from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from faker import Faker

from lunch.models import Restaurant, Menu


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.owner_client = APIClient()
        self.employee_client = APIClient()
        self.fake = Faker()

        owner_group, _ = Group.objects.get_or_create(name='Owner')
        employee_group, _ = Group.objects.get_or_create(name='Employee')

        self.owner = User.objects.create_user(username=self.fake.simple_profile()['username'],
                                              email=self.fake.email(),
                                              password=self.fake.password(),
                                              first_name=self.fake.first_name(),
                                              last_name=self.fake.last_name()
                                              )
        another_owner = User.objects.create_user(username=self.fake.simple_profile()['username'],
                                                 email=self.fake.email(),
                                                 password=self.fake.password(),
                                                 first_name=self.fake.first_name(),
                                                 last_name=self.fake.last_name()
                                                 )
        owner_group.user_set.set([self.owner, another_owner])

        self.employee = User.objects.create_user(username=self.fake.simple_profile()['username'],
                                                 email=self.fake.email(),
                                                 password=self.fake.password(),
                                                 first_name=self.fake.first_name(),
                                                 last_name=self.fake.last_name()
                                                 )
        employee_group.user_set.add(self.employee)

        self.restaurant1 = Restaurant.objects.create(name="LittleLemon", address='8 Union st.', owner=self.owner)
        self.restaurant2 = Restaurant.objects.create(name="Foreign", address='Alien', owner=another_owner)

        self.owner_client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(AccessToken.for_user(self.owner)))
        self.employee_client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(AccessToken.for_user(self.employee)))


class RestaurantAPIViewTestCase(BaseAPITestCase):

    def test_create_restaurant_by_owner(self):
        """
        Test that a user assigned as owner can create a restaurant
        """
        url = reverse('restaurants-list')
        response = self.owner_client.post(url, data={'name': 'TestRestaurant', 'address': 'TestAddress'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['data']['owner'], self.owner.id)

    def test_prohibit_creation_restaurant_by_employee(self):
        """
        Test that a user assigned as owner can create a restaurant
        """
        url = reverse('restaurants-list')
        response = self.employee_client.post(url, data={'name': 'TestRestaurant', 'address': 'TestAddress'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_for_employee(self):
        """
        Test that employee can get list oh restaurants
        """
        url = reverse('restaurants-list')
        response = self.employee_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_for_owner(self):
        """
        Test that owner can get list oh restaurants
        """
        url = reverse('restaurants-list')
        response = self.owner_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_restaurant_by_owner(self):
        """
        Test that a user assigned as owner can delete his own restaurant
        """
        url = reverse('restaurants-detail', kwargs={'pk': self.restaurant1.id})
        response = self.owner_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_prohibit_delete_restaurant_by_employee(self):
        """
        Test that a user assigned as owner can't delete a restaurant
        """
        url = reverse('restaurants-detail', kwargs={'pk': self.restaurant1.id})
        response = self.employee_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_prohibit_delete_restaurant_by_another_owner(self):
        """
        Test that a user assigned as owner can't delete a foreign restaurant
        """

        url = reverse('restaurants-detail', kwargs={'pk': self.restaurant2.id})
        response = self.owner_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_set_menu_by_owner(self):
        """
        Test that owner can set a menu for the restaurant
        """
        url = reverse('restaurants-set-menu', kwargs={'pk': self.restaurant1.id})
        response = self.owner_client.post(url, data={'items': "Item1, Item2, Item3"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_prohibit_setting_two_menu_by_owner(self):
        """
        Test that owner can not set menu for the restaurant twice
        """

        url = reverse('restaurants-set-menu', kwargs={'pk': self.restaurant1.id})

        response = self.owner_client.post(url, data={'items': "Item1, Item2, Item3"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Menu.objects.all()), 1)

        response = self.owner_client.post(url, data={'items': "Item4, Item5, Item6"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['data']['message'], ["You can only set one menu per day"])
        self.assertEqual(len(Menu.objects.all()), 1)

    def test_get_menu(self):
        """
        Test that user can get a menu for the restaurant
        """
        url = reverse('restaurants-set-menu', kwargs={'pk': self.restaurant1.id})
        self.owner_client.post(url, data={'items': "Item1, Item2, Item3"})
        url = reverse('restaurants-get-menu', kwargs={'pk': self.restaurant1.id})
        response = self.employee_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_404_if_restaurant_has_not_dayle_menu(self):
        """
        Test that user got 404 if restaurant has not dayle menu
        :return:
        """
        url = reverse('restaurants-get-menu', kwargs={'pk': self.restaurant1.id})
        response = self.employee_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MenuAPIViewTestCase(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.menu1 = Menu.objects.create(items='Item 1, Item 2, Item 3', restaurant=self.restaurant1)
        self.menu2 = Menu.objects.create(items='Item 4, Item 5, Item 6', restaurant=self.restaurant2)

    def test_list_menu(self):
        """
        Test that user can get list of menus
        """
        url = reverse('menus-list')
        response = self.employee_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_retrieve_menu(self):
        """
        Test that user can retrieve menu
        """
        url = reverse('menus-detail', kwargs={'pk': self.menu1.id})
        response = self.employee_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['restaurant'], self.restaurant1.id)

    def test_vote(self):
        """
        Test that employee can vote for menu
        """
        self.assertEqual(self.menu1.customers_vote.count(), 0)

        url = reverse('menus-vote', kwargs={'pk': self.menu1.id})
        response = self.employee_client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        menu = Menu.objects.get(pk=self.menu1.id)
        self.assertEqual(menu.customers_vote.count(), 1)

    def test_unvote(self):
        """
        Test that employee can remove his vote for menu
        """
        self.menu1.customers_vote.add(self.employee.id)
        self.assertEqual(self.menu1.customers_vote.count(), 1)

        url = reverse('menus-unvote', kwargs={'pk': self.menu1.id})
        response = self.employee_client.post(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        menu = Menu.objects.get(pk=self.menu1.id)
        self.assertEqual(menu.customers_vote.count(), 0)

    def test_prohibit_vote_by_owner(self):
        """
        Test that owner can't vote for menu
        """
        url = reverse('menus-vote', kwargs={'pk': self.menu1.id})
        response = self.owner_client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        menu = Menu.objects.get(pk=self.menu1.id)
        self.assertEqual(menu.customers_vote.count(), 0)

    def test_get_best_place(self):
        employee = User.objects.create_user(username=self.fake.simple_profile()['username'],
                                            email=self.fake.email(),
                                            password=self.fake.password(),
                                            first_name=self.fake.first_name(),
                                            last_name=self.fake.last_name()
                                            )
        Group.objects.get(name='Employee').user_set.add(employee)
        url = reverse('menus-best')

        self.menu1.customers_vote.add(self.employee.id)
        response = self.employee_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['restaurant'], self.menu1.restaurant.id)
        self.assertEqual(response.json()['data']['votes'], 1)

        self.menu2.customers_vote.set([self.employee.id, employee])
        response = self.employee_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['restaurant'], self.menu2.restaurant.id)
        self.assertEqual(response.json()['data']['votes'], 2)
