from django.contrib import admin
from django.urls import path, include
from adminpage import views

urlpatterns = [
    path('main', views.main, name='main'),
]
