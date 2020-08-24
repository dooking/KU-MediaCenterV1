from django.contrib import admin
from django.urls import path, include
from adminpage import views


# TODO:url 손보기  including 되는거라 ㅇㅇ
urlpatterns = [
    path('main', views.main, name='main'),
    path('total', views.total, name='total'),
    path('equipment', views.equipment, name='equipment'),
    path('addequipment', views.addEquipment, name='addEquipment'),
    path('qrcheck', views.qrcheck, name='qrcheck')
]
