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
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d').replace("-","")
    nextDay = (datetime.datetime.now()+datetime.timedelta(1)).strftime('%Y-%m-%d')
    camera = Equipment.objects.filter(equipType="camera",isExist=True).values('equipSemiType').distinct()
    subCamera =  Equipment.objects.filter(equipType="subcamera",isExist=True).values('equipType').distinct()
    record =  Equipment.objects.filter(equipType="record",isExist=True).values('equipType').distinct()
    light =  Equipment.objects.filter(equipType="light",isExist=True).values('equipType').distinct()
    etc =  Equipment.objects.filter(equipType="etc",isExist=True).values('equipType').distinct()
    cameraObject = makeDictionary(camera,nowDate,True)
    otherObject = makeDictionary(subCamera,nowDate,False) + makeDictionary(record,nowDate,False) + makeDictionary(light,nowDate,False) + makeDictionary(etc,nowDate,False)
    if (request.method == "POST"):
        selectDate = ''.join(request.POST['date']).replace("-","")
        year,month,day = ''.join(request.POST['date']).split("-")
        nextDay = (datetime.datetime(int(year),int(month),int(day))+datetime.timedelta(1)).strftime('%Y-%m-%d')
        cameraObject = makeDictionary(camera,selectDate,True)
        otherObject = makeDictionary(subCamera,selectDate,False) + makeDictionary(record,selectDate,False) + makeDictionary(light,selectDate,False) + makeDictionary(etc,selectDate,False)
        return render(request, '3-borrow/step1.html',{"cameraObjects":cameraObject,"otherObjects":otherObject,"selectDate": selectDate,"calendar" :''.join(request.POST['date']),"now":datetime.datetime.now().strftime('%Y-%m-%d'),"nextDay":nextDay})
    return render(request, '3-borrow/step1.html',{"cameraObjects":cameraObject,"otherObjects":otherObject,"selectDate": nowDate, "calendar" : datetime.datetime.now().strftime('%Y-%m-%d'),"now":datetime.datetime.now().strftime('%Y-%m-%d'),"nextDay":nextDay})

def makeDictionary(lists,selectDate,isCamera):
    resultObject = []
    if(isCamera):
        for semiType in lists:
            equipTypeList = Equipment.objects.filter(equipSemiType=semiType['equipSemiType']).values('equipmentName').distinct()
            resultObject.append(findName(equipTypeList,semiType['equipSemiType'],selectDate))
    else:
        for equipType in lists:
            equipTypeList = Equipment.objects.filter(equipType=equipType['equipType']).values('equipmentName').distinct()
            resultObject.append(findName(equipTypeList,equipType['equipType'],selectDate))
    return resultObject

def findName(equiments,semiType,selectDate):
    totalEquip = []
    for equiment in equiments:
        totalEquip.append(makeDict((equiment['equipmentName']),semiType,selectDate))
    result = {"type":semiType,"info":totalEquip}
    return result

def makeDict(Ename,semiType,selectDate):
    dictEquip = {}
    equipList = Equipment.objects.filter(isExist=True,equipmentName=Ename)
    dictEquip["name"] = Ename
    dictEquip["count"] = len(equipList)
    dictEquip["time1"], dictEquip["time2"] = findTime(
        Ename, selectDate, len(equipList))
    return dictEquip


def findTime(Ename, Eto, Ecount):
    todayTime = [Ecount for i in range(24)]
    tomorrowTime = [Ecount for i in range(24)]
    borrowLists = EquipmentBorrow.objects.filter(fromDate=Eto)
    for borrowList in borrowLists:
        for equipList in borrowList.equipment.replace("[","").replace("]","").replace("'","").split(","):
            [equip,count] = equipList.split(":")
            equip = equip.strip()
            count = count.strip()
            if(equip == Ename):
                for j in range(borrowList.fromDateTime,borrowList.toDateTime+2):
                    todayTime[j] -= int(count)
    borrowLists = EquipmentBorrow.objects.filter(fromDate=str(int(Eto)+1))
    for borrowList in borrowLists:
        for equipList in borrowList.equipment.replace("[","").replace("]","").replace("'","").split(","):
            [equip,count] = equipList.split(":")
            equip = equip.strip()
            count = count.strip()
            if(equip == Ename):
                for j in range(borrowList.fromDateTime,borrowList.toDateTime+2):
                    todayTime[j] -= int(count)
    # nowhi = EquipmentBorrow.objects.filter(toDate=str(int(Eto)+1))
    # for i in nowhi:
    #     if(i.equipment.equipmentName == Ename):
    #         for j in range(i.fromDateTime, i.toDateTime+1):
    #             tomorrowTime[j] -= 1
    return todayTime[9:18], tomorrowTime[9:18]


def borrow_step2(request):
    print(request.POST)
    if(request.method == "POST"):
        borrowList = "".join(request.POST['resultBorrow']).split("//")
        borrowList.pop()
        fromTime = "".join(request.POST['fromTime'])
        toTime = "".join(request.POST['toTime'])
        fromDate = "".join(request.POST['fromDate'])
        toDate = "".join(request.POST['toDate'])
        return render(request, '3-borrow/step2.html', {'borrowLists': borrowList, 'fromTime': fromTime, 'fromDate': fromDate,'toTime': toTime, 'toDate': toDate})


def borrow_finish(request):
    print(request.POST)
    if(request.method == "POST"):
        EquipmentBorrow.objects.create(
            username = Profile.objects.get(username=request.user),
            equipment="".join(request.POST['borrowList']),
            toDate="".join(request.POST['toDate']).replace("-",""),
            toDateTime=int(("".join(request.POST['toTime']))[:2]),
            fromDate="".join(request.POST['fromDate']).replace("-",""),
            fromDateTime=int(("".join(request.POST['fromTime']))[:2]),
            group="".join(request.POST['group']),
            purpose="".join(request.POST['purpose']),
            auth="".join(request.POST['auth']),
            remark="".join(request.POST['remark']),
            borrowState=1
        )
        return redirect('main')
# 로그인 권한 필요시
# @login_required(login_url='/registration/login')

# registration
