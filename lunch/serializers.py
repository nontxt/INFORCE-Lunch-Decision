from django.utils import timezone

from rest_framework import serializers

from .models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['restaurant', 'items']

    def validate(self, data):
        if Menu.objects.filter(restaurant=data['restaurant'], date=timezone.now().date()).exists():
            raise serializers.ValidationError(detail={'message': "You can only set one menu per day"})
        return data


class MostVoteMenuSerializer(MenuSerializer):
    votes = serializers.SerializerMethodField('votes_count')

    class Meta:
        model = Menu
        fields = ['restaurant', 'items', 'votes']

    def votes_count(self, obj):
        return obj.customers_vote.count()
