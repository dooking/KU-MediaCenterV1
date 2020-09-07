from django.contrib import admin
from django.urls import path, include
from adminpage import views


# TODO:
urlpatterns = [
    # main
    path('main', views.main, name='adminMain'),

    # 대여목록 전체
    path('total', views.total, name='total'),

    # 장비 추가 및 삭제
    path('equipment', views.equipment, name='equipment'),
    path('addequipment', views.addEquipment, name='addEquipment'),
    path('deleteequipment/<int:equipment_pk>',
         views.deleteEquipment, name="deleteEquipment"),
    path('brokenEquipment/<int:equipment_pk>',
         views.brokenEquipment, name="brokenEquipment"),
    path('repairEquipment/<int:equipment_pk>',
         views.repairEquipment, name="repairEquipment"),

    # 장비 대여 예약 확인 및 관리
    path('qrcheck/borrow/<int:post_pk>',
         views.qrcheckBrrow, name='qrcheckBrrow'),
    path('qrcheck/return/<int:post_pk>',
         views.qrcheckReturn, name='qrcheckReturn'),
    path('qrcheck/late/<int:post_pk>',
         views.qrcheckReturn, name='qrcheckLate'),

    # calendar
    path('calendar', views.calendar, name='calendar'),
    path('all_events/', views.all_events, name='all_events'),
]
