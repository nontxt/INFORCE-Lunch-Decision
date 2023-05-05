from django.contrib.auth.models import User


def run():
    """
    Create admin user with credentials admin|admin
    """
    User.objects.filter(username='admin').delete()
    User.objects.create_superuser(username='admin',
                                  email='admin@mail.com',
                                  password='admin',
                                  first_name='Admin',
                                  last_name='Admin')
