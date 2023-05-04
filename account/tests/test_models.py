from django.test import TestCase
from django.contrib.auth import get_user_model

from faker import Faker

from account.models import Employee, Owner

user_model = get_user_model()
fake = Faker()


class Setup(TestCase):

    def setUp(self):
        self.user = user_model.objects.create_user(username=fake.simple_profile()['username'],
                                                   email=fake.email(),
                                                   password=fake.password(),
                                                   first_name=fake.first_name(),
                                                   last_name=fake.last_name()
                                                   )


class OwnerModelTestCase(Setup):

    def test_create(self):
        """
        Test creating an owner
        """
        owner = Owner.objects.create(user=self.user)
        self.assertEqual(owner.id, 1)

    def test_delete(self):
        """
        Test deleting an owner
        """
        owner = Owner.objects.create(user=self.user)
        self.assertEqual(owner.id, 1)
        owner.delete()
        with self.assertRaises(Owner.DoesNotExist):
            Owner.objects.get(id=1)


class EmployeeModelTestCase(Setup):

    def test_create(self):
        """
        Test creating an employee
        """

        employee = Employee.objects.create(user=self.user)

        self.assertEqual(employee.id, 1)

    def test_delete(self):
        """
        Test deleting an employee
        """

        employee = Employee.objects.create(user=self.user)
        self.assertEqual(employee.id, 1)
        employee.delete()
        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(id=1)