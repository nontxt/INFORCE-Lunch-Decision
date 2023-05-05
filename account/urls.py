from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('employees/', views.employee, name='employee'),
    path('owners/', views.owner, name='owner'),
]
