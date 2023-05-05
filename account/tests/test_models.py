from django.test import TestCase
from django.contrib.auth.models import User, Group

from faker import Faker

fake = Faker()


class Setup(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username=fake.simple_profile()['username'],
                                             email=fake.email(),
                                             password=fake.password(),
                                             first_name=fake.first_name(),
                                             last_name=fake.last_name()
                                             )


class OwnerModelTestCase(Setup):

    def setUp(self):
        super().setUp()
        self.owner_group, _ = Group.objects.get_or_create(name='Owner')

    def test_assign(self):
        """
        Test assigning to owner group
        """
        self.owner_group.user_set.add(self.user)
        self.assertIn(self.owner_group, self.user.groups.all())

    def test_remove(self):
        """
        Test removing from owner group
        """
        self.owner_group.user_set.add(self.user)
        self.assertIn(self.owner_group, self.user.groups.all())
        self.owner_group.user_set.remove(self.user)
        self.assertNotIn(self.owner_group, self.user.groups.all())


class EmployeeModelTestCase(Setup):

    def setUp(self):
        super().setUp()
        self.employee_group, _ = Group.objects.get_or_create(name='Employee')

    def test_assign(self):
        """
        Test assigning to employee group
        """

        self.employee_group.user_set.add(self.user)
        self.assertIn(self.employee_group, self.user.groups.all())

    def test_remove(self):
        """
        Test removing from employee group
        """

        self.employee_group.user_set.add(self.user)
        self.assertIn(self.employee_group, self.user.groups.all())
        self.employee_group.user_set.remove(self.user)
        self.assertNotIn(self.employee_group, self.user.groups.all())
