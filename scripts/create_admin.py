from django.contrib.auth.models import User


def run():
    User.objects.filter(username='admin').delete()
    User.objects.create(username='admin',
                        email='admin@mail.com',
                        password='admin',
                        is_staff=True,
                        is_superuser=True,
                        first_name='Admin',
                        last_name='Admin')
