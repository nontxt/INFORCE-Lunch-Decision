from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from faker import Faker


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.fake = Faker()

        self.owner_group, _ = Group.objects.get_or_create(name='Owner')
        self.employee_group, _ = Group.objects.get_or_create(name='Employee')

        self.user = User.objects.create_user(username=self.fake.simple_profile()['username'],
                                             email=self.fake.email(),
                                             password=self.fake.password(),
                                             first_name=self.fake.first_name(),
                                             last_name=self.fake.last_name()
                                             )
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(AccessToken.for_user(self.user)))

    def test_access_denying_for_anonymous(self):
        """
        Test that anonymous user can not access and redirect
        """
        client = APIClient()
        url = reverse('account:employee')

        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class EmployeeAPIViewTestCase(BaseAPITestCase):

    def test_assigning(self):
        """
        Test that a user can assign to employee group
        """
        url = reverse('account:employee')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.employee_group, self.user.groups.all())

    def test_leaving(self):
        """
        Test that a user can leave an employee group
        """
        self.employee_group.user_set.add(self.user)

        url = reverse('account:employee')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.employee_group, self.user.groups.all())


class OwnerAPIViewTestCase(BaseAPITestCase):

    def test_assigning(self):
        """
        Test that a user can assign to owner group
        """
        url = reverse('account:owner')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.owner_group, self.user.groups.all())

    def test_leaving(self):
        """
        Test that a user can leave an owner group
        """
        self.owner_group.user_set.add(self.user)

        url = reverse('account:owner')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.owner_group, self.user.groups.all())
