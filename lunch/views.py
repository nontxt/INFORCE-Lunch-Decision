from django.db.models import Count
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer, MostVoteMenuSerializer
from .permissions import IsOwner, IsEmployee


class RestaurantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        if self.action in ['update', 'destroy', 'set_menu']:
            qs = self.queryset.filter(owner=self.request.user)
        else:
            qs = self.queryset
        return qs

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], url_path='menu', url_name='get-menu', detail=True)
    def get_menu(self, request, pk=None):
        restaurant = self.get_object()
        menu_qs = Menu.objects.filter(date__gte=timezone.now().date(), restaurant=restaurant).first()
        serializer = MenuSerializer(menu_qs)
        if serializer.data['restaurant'] is None:
            raise NotFound('The restaurant has not a day menu yet.')
        return Response(serializer.data)

    @action(methods=['post'], url_path='set-menu', url_name='set-menu', detail=True)
    def set_menu(self, request, pk=None):
        restaurant = self.get_object()
        data = self.request.data.copy()
        data['restaurant'] = restaurant.id
        serializer = MenuSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MenuViewSet(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsEmployee]
    queryset = Menu.objects.filter(date__gte=timezone.now().date())
    serializer_class = MenuSerializer

    @action(methods=['post'], detail=True)
    def vote(self, request, pk=None):
        menu = self.get_object()
        menu.customers_vote.add(request.user.id)
        return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def unvote(self, request, pk=None):
        menu = self.get_object()
        menu.customers_vote.remove(request.user.id)
        return Response({'message': 'ok'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_name='best', url_path='best')
    def get_best(self, request):
        best_place = self.get_queryset().annotate(votes=Count('customers_vote')).order_by('-votes').first()

        serializer = MostVoteMenuSerializer(best_place, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
