from django.shortcuts import render, redirect
from .models import Profile, Equipment, Studio, EquipmentBorrow, StudioBorrow
import datetime
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

# 0 - Adming
# 1 - startpage


def main(request):
    return render(request, '1-startpage/main.html')

# 2 - Introduce


def introduce(request):
    return render(request, '2-introduce/intro.html')

# 3 - Borrow


@csrf_exempt
def step1(request):
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d').replace("-", "")
    totalDslr = []
    dslr = Equipment.objects.filter(
        isExist=True, equipType="DSLR").values('equipmentName').distinct()
    totalDslr = findName(dslr, nowDate)
    totalCamcorder = []
    camcorder = Equipment.objects.filter(
        isExist=True, equipType="Camcorder").values('equipmentName').distinct()
    totalCamcorder = findName(camcorder, nowDate)
    if (request.method == "POST"):
        print(request.POST)
        selectDate = ''.join(request.POST['date']).replace("-", "")
        dslr = Equipment.objects.filter(
            isExist=True, equipType="DSLR").values('equipmentName').distinct()
        totalDslr = findName(dslr, selectDate)
        camcorder = Equipment.objects.filter(
            isExist=True, equipType="Camcorder").values('equipmentName').distinct()
        totalCamcorder = findName(camcorder, nowDate)
        return render(request, '3-borrow/step1.html', {"totalDslr": totalDslr, "totalCamcorder": totalCamcorder, "selectDate": selectDate})
    print(totalDslr)
    return render(request, '3-borrow/step1.html', {"totalDslr": totalDslr, "totalCamcorder": totalCamcorder, "selectDate": nowDate})


def findName(equiments, selectDate):
    totalEquip = []
    for equiment in equiments:
        print(equiment)
        totalEquip.append(makeDict((equiment['equipmentName']), selectDate))
    return totalEquip


def makeDict(Ename, selectDate):
    dictEquip = {}
    equipList = Equipment.objects.filter(isExist=True, equipmentName=Ename)
    dictEquip["name"] = Ename
    dictEquip["count"] = len(equipList)
    dictEquip["time1"], dictEquip["time2"] = findTime(
        Ename, selectDate, len(equipList))
    return dictEquip


def findTime(Ename, Eto, Ecount):
    todayTime = [Ecount for i in range(24)]
    tomorrowTime = [Ecount for i in range(24)]
    nowhi = EquipmentBorrow.objects.filter(toDate=Eto)
    for i in nowhi:
        if(i.equipment.equipmentName == Ename):
            print("hi")
            for j in range(i.fromDateTime, i.toDateTime+1):
                todayTime[j] -= 1
    nowhi = EquipmentBorrow.objects.filter(toDate=str(int(Eto)+1))
    for i in nowhi:
        if(i.equipment.equipmentName == Ename):
            for j in range(i.fromDateTime, i.toDateTime+1):
                tomorrowTime[j] -= 1
    return todayTime[9:18], tomorrowTime[9:18]


def borrow_step2(request):
    if(request.method == "POST"):
        print(request.POST)
        camera = "".join(request.POST['cam'])
        fromTime = "".join(request.POST['fromTime'])
        toTime = "".join(request.POST['toTime'])
        toDate = "".join(request.POST['toDate'])
        return render(request, '3-borrow/step2.html', {'camera': camera, 'fromTime': fromTime, 'toTime': toTime, 'toDate': toDate})


def borrow_finish(request):
    if(request.method == "POST"):
        print(request.POST['camera'])
        equipment = Equipment.objects.filter(
            equipmentName=request.POST['camera']).order_by('equipmentName').first()
        EquipmentBorrow.objects.create(
            equipment=equipment,
            toDate="".join(request.POST['toDate']),
            toDateTime=int(("".join(request.POST['toTime']))[:2]),
            fromDate="".join(request.POST['toDate']),
            fromDateTime=int(("".join(request.POST['fromTime']))[:2]),
            group="".join(request.POST['group']),
            purpose="".join(request.POST['purpose']),
            auth="".join(request.POST['auth']),
            willBorrow=True
        )
        return redirect('main')
# 로그인 권한 필요시
# @login_required(login_url='/registration/login')

# registration
