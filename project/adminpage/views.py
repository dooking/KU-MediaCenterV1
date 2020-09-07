# from django.shortcuts import render, redirect
from app.models import Equipment, EquipmentBorrow, Profile
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

# TODO: 예약 현황 관리 -> 상태별로 띄워주는 것으로 구현
# TODO: 전체 반납 내역 관리 -> 누가 이걸 작성했는지도 알아야됨
# TODO: 장비 모델 추가 및 삭제 (고장 포함) (장비 모델 crud)
# TODO: 슈퍼 사용자가 근장한테 권한 주는 페이지
# TODO: QRcode 입력해서 대여 장비의 상태 바꾸기

from django.http import HttpResponse
from .models import CalendarEvent
from project.util import events_to_json, calendar_options
from django.core import serializers

OPTIONS = """{  timeFormat: "HH",
                columnHeaderText: function(date) {
                    let weekList = ["일", "월", "화", "수", "목", "금", "토"];
                    return weekList[date.getDay()];
                },
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'month,agendaWeek,agendaDay',
                },
                
                allDaySlot: true,
                firstDay: 0,
                weekMode: 'liquid',
                slotMinutes: 15,
                defaultEventMinutes: 30,
                minTime: 0,
                maxTime: 24,
                editable: false,
                dayClick: function(date, allDay, jsEvent, view) {
                    if (allDay) {
                        $('#calendar').fullCalendar('gotoDate', date)
                        $('#calendar').fullCalendar('changeView', 'agendaDay')
                    }
                },
                eventClick: function(event, jsEvent, view) {
                    if (view.name == 'month') {
                        $('#calendar').fullCalendar('gotoDate', event.start)
                        $('#calendar').fullCalendar('changeView', 'agendaDay')
                    }
                },
                
                
            }"""


def calendar(request):
    event_url = 'all_events/'
    return render(request, 'calendar.html', {'calendar_config_options': calendar_options(event_url, OPTIONS)})


def all_events(request):
    events = CalendarEvent.objects.all()
    eee = serializers.serialize('json', events)
    print(eee)
    print(events_to_json(events))

    equipmentBorrows = EquipmentBorrow.objects.all()
    e = serializers.serialize('json', equipmentBorrows)
    print(e)

    return HttpResponse(events_to_json(events), content_type='application/json')


def main(request):
    # 대여 목록의 state를 0,1,2로 구분해놨고, 이를 필터링해주고 랜더링 해주면 됨
    # 각각의 cell에 update해주는 창 하나 만들기 확인 누르면 다시 랜더링 되는걸로
    state0 = EquipmentBorrow.objects.filter(borrowState=0)
    state1 = EquipmentBorrow.objects.filter(borrowState=1)
    state2 = EquipmentBorrow.objects.filter(borrowState=2)

    return render(request, "main.html", {
        "state0s": state0, "state1s": state1, "state2s": state2
    })


def total(request):
    # 모든 대여내역 다 보여주면 됨
    borrows_all = EquipmentBorrow.objects.all()

    q = request.GET.get('q', '')
    if q:
        borrows_all = borrows_all.filter(Q(username__name__icontains=q)|Q(username__major__icontains=q)|Q(equipment__icontains=q)|Q(fromDate__icontains=q)|Q(toDate__icontains=q)|Q(purpose__icontains=q)|Q(auth__icontains=q)|Q(remark__icontains=q))
    page = int(request.GET.get('p', 1))
    paginator = Paginator(borrows_all, 5) 
    borrows = paginator.get_page(page)

    return render(request, "total.html", {"borrows":borrows, "range":range(1, borrows.paginator.num_pages+1), "low_range":borrows.number-2, "high_range":borrows.number+2})


def equipment(request):
    # 장비 목록 다 보여주면 됨
    # 장비 추가는 따로 탭을 만들거고
    # 장비 삭제 및 사용 불가 처리는 여기서 할 수 있도록
    # 함수는 따로 뺴야됨
    equipments = Equipment.objects.all()
    return render(request, "equipment.html", {"equipments": equipments})


def qrcheckBrrow(request, post_pk):
    currentEquipment = EquipmentBorrow.objects.filter(pk=post_pk)
    print(currentEquipment)
    if request.method == "POST":
        currentEquipment.update(
            equipment=request.POST['equipments'], borrowState=1)
        return redirect('main')
    return render(request, "qrcheckBorrow.html", {'currentEquipment': currentEquipment[0]})


def qrcheckReturn(request, post_pk):
    currentEquipment = EquipmentBorrow.objects.filter(pk=post_pk)
    if request.method == "POST":
        currentEquipment.update(
            equipment=request.POST['equipments'], borrowState=1)
        return redirect('main')
    return render(request, "qrcheckReturn.html", {'currentEquipment': currentEquipment[0]})


def addEquipment(request):
    if request.method == 'POST':
        foundEquipByserial = Equipment.objects.filter(
            serialNumber=request.POST['serialNumber'])

        if len(foundEquipByserial) == 0:
            Equipment.objects.create(
                equipmentName=request.POST['equipmentName'],
                serialNumber=request.POST['serialNumber'],
                equipType=request.POST['equipType'],
                equipSemiType=request.POST['equipSemiType'],
                isExist=True,
                borrowState=0
            )
            msg = '정상적으로 제품을 등록하였습니다.'
            return render(request, 'addEquipment.html', {"msg": msg})
        else:
            error = '이미 존재하는 serial number 입니다.'
            return render(request, 'addEquipment.html', {"msg": error})
    return render(request, "addequipment.html")


def deleteEquipment(request, equipment_pk):
    deleteEquipment = Equipment.objects.get(pk=equipment_pk)
    deleteEquipment.delete()
    return redirect('equipment')


def brokenEquipment(request, equipment_pk):
    Equipment.objects.filter(pk=equipment_pk).update(isExist=False)
    return redirect('equipment')

def repairEquipment(request, equipment_pk):
    Equipment.objects.filter(pk=equipment_pk).update(isExist=True)
    return redirect('equipment')

def adminAuth(request):
    users = Profile.objects.all()
    return render(request, "adminAuth.html", {"users": users})

def adminAddAuth(request, user_pk):
    Profile.objects.filter(pk = user_pk).update(isAuth=1)
    return redirect('adminAuth')

def adminDeleteAuth(request, user_pk):
    Profile.objects.filter(pk = user_pk).update(isAuth=0)
    return redirect('adminAuth')

def adminAddSuperAuth(request, user_pk):
    Profile.objects.filter(pk = user_pk).update(isAuth=2)
    return redirect('adminAuth')

