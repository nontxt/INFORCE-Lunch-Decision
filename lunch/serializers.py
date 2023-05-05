from django.utils import timezone

from rest_framework import serializers

from .models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField(read_only=True)  # User friendly name

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'owner_name', 'owner']
        extra_kwargs = {
            'owner': {'write_only': True}
        }

    def get_owner_name(self, obj):
        return f"{obj.owner.first_name} {obj.owner.last_name}"


class MenuSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.StringRelatedField(source='restaurant', read_only=True)   # User friendly name

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'items', 'restaurant_name']
        extra_kwargs = {
            'restaurant': {'write_only': True}
        }

    def validate(self, data):
        """
        Validate that owner creates one menu per day
        """
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
