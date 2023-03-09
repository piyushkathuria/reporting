from django.urls import path

from . import views
from reporting.views import *
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('customerlist', views.customer_list, name='customerlist'),
]
