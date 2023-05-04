from django.contrib.auth import get_user_model

from faker import Faker

from account.models import Employee, Owner


def run():
    fake = Faker()
    user_model = get_user_model()

    user_model.objects.all().delete()
    user_model.objects.create_user(username='admin',
                                   email='admin@example.com',
                                   password='admin',
                                   first_name='Admin',
                                   last_name='Admin',
                                   is_staff=True,
                                   is_superuser=True
                                   )
    for _ in range(100):
        user_model.objects.create_user(username=fake.simple_profile()['username'],
                                       email=fake.email(),
                                       password=fake.password(),
                                       first_name=fake.first_name(),
                                       last_name=fake.last_name()
                                       )
    users = user_model.objects.all()

    for i, user in enumerate(users):
        if i < 10:
            Owner.objects.create(user=user)
        else:
            Employee.objects.create(user=user)