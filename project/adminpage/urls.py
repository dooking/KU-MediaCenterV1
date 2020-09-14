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
    path('equipment_qr/<int:equipment_pk>', views.equipment_qr, name='equipment_qr'),
    path('deleteequipment/<int:equipment_pk>',
         views.deleteEquipment, name="deleteEquipment"),
    path('detailEquipment/<int:equipment_pk>',
         views.detailEquipment, name="detailEquipment"),
    path('brokenEquipment/<int:equipment_pk>',
         views.brokenEquipment, name="brokenEquipment"),
    path('repairEquipment/<int:equipment_pk>',
         views.repairEquipment, name="repairEquipment"),

    # 공간 추가 및 삭제
    path('studio', views.studio, name='studio'),
    path('addstudio', views.addStudio, name='addStudio'),
    path('studio_qr/<int:studio_pk>', views.studio_qr, name='studio_qr'),
    path('deletestudio/<int:studio_pk>',
         views.deleteStudio, name="deleteStudio"),
    path('detailstudio/<int:studio_pk>',
         views.detailStudio, name="detailStudio"),
    path('brokenstudio/<int:studio_pk>',
         views.brokenStudio, name="brokenStudio"),
    path('repairstudio/<int:studio_pk>',
         views.repairStudio, name="repairStudio"),

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

    #관리자 권한 부여
    path('adminAuth', views.adminAuth, name='adminAuth'),
    path('adminAddAuth/<int:user_pk>', views.adminAddAuth, name='adminAddAuth'),
    path('adminDeleteAuth/<int:user_pk>',
         views.adminDeleteAuth, name="adminDeleteAuth"),

]
