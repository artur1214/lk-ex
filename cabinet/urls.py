from django.contrib import admin
from django.urls import path
from .views import index, redirect_to_pp, register_view, user_register, cabinet_view

urlpatterns = [
    path('', index),
    path('register/', register_view),
    path('priceplan/<str:key>/', redirect_to_pp),
    path('api/register/', user_register),
    path('cabinet/', cabinet_view),

]
