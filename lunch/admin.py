from django.contrib import admin
from django.db.models import Count
from .models import Restaurant, Menu

admin.site.register(Restaurant)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['restaurant_name', 'votes']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(votes=Count('customers_vote')).order_by('-votes')
        return qs

    def restaurant_name(self, obj):
        return obj.restaurant.name

    def votes(self, obj):
        return obj.votes
