from django.contrib import admin

from .models import Employee, Owner


admin.site.register([Employee, Owner])
