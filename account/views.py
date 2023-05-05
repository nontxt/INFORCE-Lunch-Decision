from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

employee_group, _ = Group.objects.get_or_create(name='Employee')
owner_group, _ = Group.objects.get_or_create(name='Owner')


@api_view(['post', 'delete'])
@login_required
def employee(request):
    if request.method == 'POST':
        employee_group.user_set.add(request.user)
        return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)
    else:
        employee_group.user_set.remove(request.user)
        return Response({'message': 'ok'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['post', 'delete'])
@login_required
def owner(request):
    if request.method == 'POST':
        owner_group.user_set.add(request.user)
        return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)
    else:
        owner_group.user_set.remove(request.user)
        return Response({'message': 'ok'}, status=status.HTTP_204_NO_CONTENT)
