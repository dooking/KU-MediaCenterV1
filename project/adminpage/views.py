# from django.shortcuts import render, redirect
from app.models import Equipment, EquipmentBorrow, Profile, Studio, StudioBorrow
from django.shortcuts import render, redirect
from django.db.models import Q
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
from django.core.paginator import Paginator
from django.views.generic import ListView
import datetime

OPTIONS = """{  timeFormat: "H:mm",
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'month,agendaWeek,agendaDay',
                },
                allDaySlot: false,
                firstDay: 0,
                weekMode: 'liquid',
                slotMinutes: 15,
                defaultEventMinutes: 30,
                minTime: 8,
                maxTime: 20,
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
    # 대여 목록의 state를 0,1,2로 구분해놨고, 이를 필터링해
    # 주고 랜더링 해주면 됨
    # 각각의 cell에 update해주는 창 하나 만들기 확인 누르면 다시 랜더링 되는걸로
    # TODO:자동으로 연체 되게 업데이트 해주는것 해야됨
    equipLists = EquipmentBorrow.objects.filter(Q(borrowState=0)|Q(borrowState=1)).order_by('fromDate')
    for equip in equipLists:
        now = datetime.datetime.now()
        nowDate = int(now.strftime("%Y-%m-%d").replace("-", ""))
        nowTime = int(now.hour)
        toDate,toDateTime = int(equip.toDate), int(equip.toDateTime)
        if((toDate == nowDate and toDateTime < nowTime) or (toDate < nowDate)):
            lateEquipment = EquipmentBorrow.objects.filter(pk=equip.pk)
            lateEquipment.update(
                borrowState = 2
            )
        
    state0 = makeLists(EquipmentBorrow.objects.filter(borrowState=0))
    state1 = makeLists(EquipmentBorrow.objects.filter(borrowState=1))
    state2 = makeLists(EquipmentBorrow.objects.filter(borrowState=2))
    return render(request, "main.html", {
        "state0s": state0, "state1s": state1, "state2s": state2
    })

def main_studio(request):
    # 대여 목록의 state를 0,1,2로 구분해놨고, 이를 필터링해
    # 주고 랜더링 해주면 됨
    # 각각의 cell에 update해주는 창 하나 만들기 확인 누르면 다시 랜더링 되는걸로
    # TODO:자동으로 연체 되게 업데이트 해주는것 해야됨
    studioLists = StudioBorrow.objects.filter(Q(studioState=0)|Q(studioState=1))
    for studio in studioLists:
        now = datetime.datetime.now()
        nowDate = int(now.strftime("%Y-%m-%d").replace("-", ""))
        nowTime = int(now.hour)
        toDate,toDateTime = int(studio.toDate), int(studio.toDateTime)
        if((toDate == nowDate and toDateTime < nowTime) or (toDate < nowDate)):
            lateStudio = StudioBorrow.objects.filter(pk=studio.pk)
            lateStudio.update(
                studioState = 2
            )
        
    state0 = makeLists(StudioBorrow.objects.filter(studioState=0))
    state1 = makeLists(StudioBorrow.objects.filter(studioState=1))
    state2 = makeLists(StudioBorrow.objects.filter(studioState=2))
    return render(request, "main_studio.html", {
        "state0s": state0, "state1s": state1, "state2s": state2
    })


def makeLists(nowState):
    results = []
    if len(nowState) > 0:
        for state in nowState:
            temp = {}
            # equipLists = []
            # for i in state.equipment.replace("[", " ").replace("]", " ").replace("'", " ").split(","):
            #     equipments = {}
            #     equipments["equip"] = i.strip().split(":")[0].strip()
            #     equipments["count"] = i.strip().split(":")[1].strip()
            #     equipLists.append(equipments)
            temp["pk"] = state.pk
            temp["username"] = state.username.name
            temp["major"] = state.username.major
            # temp["equips"] = equipLists
            temp["fromDateYear"] = state.fromDate[:4]
            temp["fromDateMonth"] = state.fromDate[4:6]
            temp["fromDateDay"] = state.fromDate[6:8]
            temp["fromDateTime"] = state.fromDateTime
            temp["toDateYear"] = state.toDate[:4]
            temp["toDateMonth"] = state.toDate[4:6]
            temp["toDateDay"] = state.toDate[6:8]
            temp["toDateTime"] = state.toDateTime
            results.append(temp)
    return results


def total(request):
    # 모든 대여내역 다 보여주면 됨
    totalBrrows_all = EquipmentBorrow.objects.all().order_by('toDate')
    query = request.GET.get('query')
    if(query):
        filter_Brrows = filter_query(True, query,totalBrrows_all)
        paginator = Paginator(filter_Brrows, 5) 
    else:
        paginator = Paginator(totalBrrows_all, 5)
    page = int(request.GET.get('page', 1)) 
    totalBrrows = paginator.get_page(page)
    if(request.method == "POST"):
        equipPK = "".join(request.POST["equipPK"])
        editEquipList = EquipmentBorrow.objects.filter(pk=equipPK)
        editEquipList.update(
            realDate = "".join(request.POST["realDate"]),
            realDateTime = "".join(request.POST["realDateTime"]),
            group = "".join(request.POST["group"]),
            phone = "".join(request.POST["phone"]),
            purpose = "".join(request.POST["purpose"]),
            auth = "".join(request.POST["auth"]),
            remark = "".join(request.POST["remark"]),
            borrowState = "".join(request.POST["borrowState"]),
        )
    return render(request, "total.html", {"borrows": totalBrrows,"query":query})

def total_studio(request):
    # 모든 대여내역 다 보여주면 됨
    totalBrrows_all = StudioBorrow.objects.all().order_by('toDate')
    query = request.GET.get('query')
    if(query):
        filter_Brrows = filter_query(False, query,totalBrrows_all)
        paginator = Paginator(filter_Brrows, 5) 
    else:
        paginator = Paginator(totalBrrows_all, 5)
    page = int(request.GET.get('page', 1)) 
    totalBrrows = paginator.get_page(page)
    if(request.method == "POST"):
        equipPK = "".join(request.POST["equipPK"])
        editStudioList = StudioBorrow.objects.filter(pk=equipPK)
        editStudioList.update(
            realDate = "".join(request.POST["realDate"]),
            realDateTime = "".join(request.POST["realDateTime"]),
            group = "".join(request.POST["group"]),
            phone = "".join(request.POST["phone"]),
            purpose = "".join(request.POST["purpose"]),
            auth = "".join(request.POST["auth"]),
            remark = "".join(request.POST["remark"]),
            studioState = "".join(request.POST["borrowState"]),
        )
    return render(request, "total_studio.html", {"borrows": totalBrrows ,"query":query})

# def total_studio(request):
#     # 모든 대여내역 다 보여주면 됨
#     totalBrrows = StudioBorrow.objects.all().order_by('toDate')
#     if(request.method == "POST"):
#         query = "".join(request.POST['query'])
#         filter_Brrows = filter_query(False, query,totalBrrows)
#         return render(request, "total_studio.html", {"borrows": filter_Brrows})
#     return render(request, "total_studio.html", {"borrows": totalBrrows})

def filter_query(isEquip, query, totalBrrows):
    results = []
    for brrows in totalBrrows:
        if(isEquip):
            if(query in str(brrows.equipment)):
                results.append(brrows)
                continue
        else:
            if(query in str(brrows.studio)):
                results.append(brrows)
                continue
        if(query in str(brrows.username) or query in str(brrows.fromDate) or query in str(brrows.toDate) or query in str(brrows.auth)):
            results.append(brrows)
    return results

def equipment(request):
    # 장비 목록 다 보여주면 됨
    # 장비 추가는 따로 탭을 만들거고
    # 장비 삭제 및 사용 불가 처리는 여기서 할 수 있도록
    # 함수는 따로 뺴야됨
    equipments = Equipment.objects.all()
    if(request.method == "POST"):
        print(request.POST)
        equipType = "".join(request.POST['equipType'])
        equipSemiType = "".join(request.POST['equipSemiType'])
        equipmentName = "".join(request.POST['equipmentName'])
        serialNumber = "".join(request.POST['serialNumber'])
        borrowState = "".join(request.POST['borrowState'])
        remark = "".join(request.POST['remark'])
        equipPK = "".join(request.POST['equipPK'])
        print(equipType,equipSemiType,equipmentName,borrowState,equipPK)
        editEquip = Equipment.objects.filter(pk=equipPK)
        editEquip.update(
            equipType = equipType,
            equipSemiType = equipSemiType,
            equipmentName = equipmentName,
            serialNumber = serialNumber,
            borrowState = borrowState,
            remark = remark
        )
    return render(request, "equipment.html", {"equipments": equipments})

def studio(request):
    # 장비 목록 다 보여주면 됨
    # 장비 추가는 따로 탭을 만들거고
    # 장비 삭제 및 사용 불가 처리는 여기서 할 수 있도록
    # 함수는 따로 뺴야됨
    studios = Studio.objects.all()
    if(request.method == "POST"):
        print(request.POST)
        studioType = "".join(request.POST['studioType'])
        studioName = "".join(request.POST['studioName'])
        borrowState = "".join(request.POST['borrowState'])
        remark = "".join(request.POST['remark'])
        studioPK = "".join(request.POST['studioPK'])
        # print(equipType,equipSemiType,equipmentName,borrowState,equipPK)
        editStudio = Studio.objects.filter(pk=studioPK)
        editStudio.update(
            studioType = studioType,
            studioName = studioName,
            borrowState = borrowState,
            remark = remark
        )
    return render(request, "studio.html", {"studios": studios})


def equipment_qr(request, equipment_pk):
    currentEquipment = Equipment.objects.get(pk=equipment_pk)
    return render(request, "equipment_qr.html", {"currentEquipment": currentEquipment})


def qrcheckBrrow(request, post_pk):
    currentEquipment = EquipmentBorrow.objects.filter(pk=post_pk)
    if request.method == "POST":
        #카메라^DSLR^DSLR (Canon EOS-80A)^1  @@카메라^DSLR^DSLR (Canon EOS-80A)^1@@카메라^DSLR^DSLR (Canon EOS-80A)^1
        equipments = request.POST['equipments']
        for equipment in equipments.split("@@"):
            [eName, eNumber, eType, eSemiType] = equipment.split("^")
            eType = eType.replace("\ufeff", "")
            EquipmentState = Equipment.objects.filter(
                Q(equipType=eType), Q(serialNumber=eNumber))
            EquipmentState.update(
                borrowState=1
            )
        currentEquipment.update(
            equipmentList=equipments, borrowState=1)
        return redirect('adminMain')
    return render(request, "qrcheckBorrow.html", {'currentEquipment': currentEquipment[0]})


def qrcheckReturn(request, post_pk):
    currentEquipment = EquipmentBorrow.objects.filter(pk=post_pk)
    if request.method == "POST":
        equipments = request.POST['equipments']
        for equipment in equipments.split("@@"):
            [eName, eNumber, eType, eSemiType] = equipment.split("^")
            eType = eType.replace("\ufeff", "")
            EquipmentState = Equipment.objects.filter(
                Q(equipType=eType), Q(serialNumber=eNumber))
            now = datetime.datetime.now()
            EquipmentState.update(
                borrowState=0
            )
        realDate = int(now.strftime("%Y-%m-%d").replace("-", ""))
        realDateTime = int(now.hour)
        currentEquipment.update(
            equipmentList=equipments, realDate=realDate, realDateTime=realDateTime, borrowState=3)

        return redirect('adminMain')
    return render(request, "qrcheckReturn.html", {'currentEquipment': currentEquipment[0]})


def qrcheckLate(request, post_pk):
    currentEquipment = EquipmentBorrow.objects.filter(pk=post_pk)
    if request.method == "POST":
        equipments = request.POST['equipments']
        for equipment in equipments.split("@@"):
            [eType, eSemiType, eName, eNumber] = equipment.split("^")
            eType = eType.replace("\ufeff", "")
            EquipmentState = Equipment.objects.filter(
                Q(equipmentName=eName), Q(equipType=eType), Q(serialNumber=eNumber))
            EquipmentState.update(
                borrowState=0
            )
        currentEquipment.update(
            equipmentList=equipments, borrowState=3)
        return redirect('adminMain')
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
            return redirect('equipment')
        else:
            error = '이미 존재하는 serial number 입니다.'
            return render(request, 'addEquipment.html', {"msg": error})
    return render(request, "addequipment.html")

def addStudio(request):
    if request.method == 'POST':
        Studio.objects.create(
            studioName=request.POST['studioName'],
            studioType=request.POST['studioType'],
            isExist=True,
            studioState=0
        )
        return redirect('studio')
    return render(request, "addstudio.html")


# 장비대여 리스트 수정 및 삭제 
def deleteTotal(request, equipment_pk):
    deleteEquipList = EquipmentBorrow.objects.get(pk=equipment_pk)
    deleteEquipList.delete()
    return redirect('total')

def detailTotal(request, equipment_pk):
    EquipList = EquipmentBorrow.objects.get(pk=equipment_pk)
    return render(request, 'detailTotal.html',{'EquipList':EquipList})

# 공간대여 리스트 수정 및 삭제 
def deleteTotalStudio(request, equipment_pk):
    deleteStudioList = StudioBorrow.objects.get(pk=equipment_pk)
    deleteStudioList.delete()
    return redirect('total_studio')

def detailTotalStudio(request, equipment_pk):
    StudioList = StudioBorrow.objects.get(pk=equipment_pk)
    return render(request, 'detailTotalStudio.html',{'StudioList':StudioList})



def deleteEquipment(request, equipment_pk):
    deleteEquipment = Equipment.objects.get(pk=equipment_pk)
    deleteEquipment.delete()
    return redirect('equipment')


def detailEquipment(request, equipment_pk):
    equipment = Equipment.objects.get(pk=equipment_pk)
    return render(request, 'detailEquipment.html',{'Equipment':equipment})
    
def brokenEquipment(request, equipment_pk):
    Equipment.objects.filter(pk=equipment_pk).update(isExist=False)
    equipment = Equipment.objects.get(pk=equipment_pk)
    return render(request, 'detailEquipment.html',{'Equipment':equipment})


def repairEquipment(request, equipment_pk):
    Equipment.objects.filter(pk=equipment_pk).update(isExist=True)
    equipment = Equipment.objects.get(pk=equipment_pk)
    print(equipment)
    print("hihi")
    return render(request, 'detailEquipment.html',{'Equipment':equipment})

def deleteStudio(request, studio_pk):
    deleteStudio = Studio.objects.get(pk=studio_pk)
    deleteStudio.delete()
    return redirect('studio')


def detailStudio(request, studio_pk):
    studio = Studio.objects.get(pk=studio_pk)
    return render(request, 'detailStudio.html',{'studio':studio})
    
def brokenStudio(request, studio_pk):
    Studio.objects.filter(pk=studio_pk).update(isExist=False)
    studio = Studio.objects.get(pk=studio_pk)
    return render(request, 'detailStudio.html',{'studio':studio})


def repairStudio(request, studio_pk):
    Studio.objects.filter(pk=studio_pk).update(isExist=True)
    studio = Studio.objects.get(pk=studio_pk)
    print(studio)
    print("hihi")
    return render(request, 'detailStudio.html',{'studio':studio})


def adminAuth(request):
    users = Profile.objects.all()
    return render(request, "adminAuth.html", {"users": users})


def adminAddAuth(request, user_pk):
    Profile.objects.filter(pk=user_pk).update(isAuth=1)
    return redirect('adminAuth')


def adminDeleteAuth(request, user_pk):
    Profile.objects.filter(pk=user_pk).update(isAuth=0)
    return redirect('adminAuth')


def adminAddSuperAuth(request, user_pk):
    Profile.objects.filter(pk=user_pk).update(isAuth=2)
    return redirect('adminAuth')
