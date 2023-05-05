from django.contrib.auth.models import Group


def run():
    """
    Create necessary groups
    """
    Group.objects.all().delete()
    Group.objects.create(name='Employee')
    Group.objects.create(name='Owner')
