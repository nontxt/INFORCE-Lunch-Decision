from django.contrib import admin

from .models import Restaurant, DailyMenu


admin.site.register([Restaurant, DailyMenu])
