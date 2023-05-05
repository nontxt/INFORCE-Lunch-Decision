from django.contrib.auth.models import User, Group

from faker import Faker


def run():
    fake = Faker()

    User.objects.all().delete()

    for _ in range(100):
        User.objects.create_user(username=fake.simple_profile()['username'],
                                 email=fake.email(),
                                 password=fake.password(),
                                 first_name=fake.first_name(),
                                 last_name=fake.last_name()
                                 )
    employees_group = Group.objects.get(name='Employee')
    owners_group = Group.objects.get(name='Owner')
    for i, user in enumerate(User.objects.all()):
        if i < 10:
            owners_group.user_set.add(user)
        else:
            employees_group.user_set.add(user)
