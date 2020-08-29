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
def borrow_step1(request):
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d').replace("-", "")
    nextDay = (datetime.datetime.now() +
               datetime.timedelta(1)).strftime('%Y-%m-%d')
    camera = Equipment.objects.filter(equipType="카메라", isExist=True).values('equipType').distinct()
    subCamera = Equipment.objects.filter(equipType="카메라 보조 장치", isExist=True).values('equipType').distinct()
    record = Equipment.objects.filter(equipType="녹음 장비", isExist=True).values('equipType').distinct()
    light = Equipment.objects.filter(equipType="조명", isExist=True).values('equipType').distinct()
    etc = Equipment.objects.filter(equipType="기타 부속", isExist=True).values('equipType').distinct()
    #cameraObject = makeDictionary(camera, nowDate)
    otherObject = makeDictionary(camera, nowDate) +makeDictionary(subCamera, nowDate) + makeDictionary(record, nowDate) + makeDictionary(light, nowDate) + makeDictionary(etc, nowDate)

    if (request.method == "POST"):
        selectDate = ''.join(request.POST['selectDate']).replace("-", "")
        year, month, day = ''.join(request.POST['selectDate']).split("-")
        nextDay = (datetime.datetime(int(year), int(month), int(
            day))+datetime.timedelta(1)).strftime('%Y-%m-%d')
        #cameraObject = makeDictionary(camera, selectDate)
        otherObject = makeDictionary(camera, selectDate) + makeDictionary(subCamera, selectDate) + makeDictionary(record, selectDate) + makeDictionary(light, selectDate) + makeDictionary(etc, selectDate)
        return render(request, '3-borrow/step1.html', {"otherObjects": otherObject, "selectDate": selectDate, "calendar": ''.join(request.POST['selectDate']), "now": datetime.datetime.now().strftime('%Y-%m-%d'), "nextDay": nextDay})
    return render(request, '3-borrow/step1.html', {"otherObjects": otherObject, "selectDate": nowDate, "calendar": datetime.datetime.now().strftime('%Y-%m-%d'), "now": datetime.datetime.now().strftime('%Y-%m-%d'), "nextDay": nextDay})


def makeDictionary(lists, selectDate):
    resultObject = []
    # if(isCamera):
    #     for semiType in lists:
    #         equipTypeList = Equipment.objects.filter(
    #             equipSemiType=semiType['equipSemiType']).values('equipmentName').distinct()
    #         resultObject.append(
    #             findName(equipTypeList, semiType['equipSemiType'], selectDate))
    # else:
    for equipType in lists:
        equipTypeList = Equipment.objects.filter(equipType=equipType['equipType']).values('equipmentName').distinct()
        resultObject.append(findName(equipTypeList, equipType['equipType'], selectDate))
    return resultObject


def findName(equiments, semiType, selectDate):
    totalEquip = []
    for equiment in equiments:
        totalEquip.append(
            makeDict((equiment['equipmentName']), semiType, selectDate))
    result = {"type": semiType, "info": totalEquip}
    return result


def makeDict(Ename, semiType, selectDate):
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
    # 오늘 현황 (오늘 반납할 사람 + 빌리는 사람)
    todayReturn = EquipmentBorrow.objects.filter(fromDate=str(int(Eto)-1),toDate=Eto)
    todayBorrow = EquipmentBorrow.objects.filter(fromDate=Eto)
    for borrowList in todayReturn:
        for equipList in borrowList.equipment.replace("[", "").replace("]", "").replace("'", "").split(","):
            [equip, count] = equipList.split(":")
            equip = equip.strip()
            count = count.strip()
            if(equip == Ename):
                for j in range(borrowList.toDateTime+2):
                    todayTime[j] -= int(count)
    for borrowList in todayBorrow:
        for equipList in borrowList.equipment.replace("[", "").replace("]", "").replace("'", "").split(","):
            print(Ename, equipList)
            [equip, count] = equipList.split(":")
            equip = equip.strip()
            count = count.strip()
            if(equip == Ename):
                if(int(borrowList.fromDate) < int(borrowList.toDate)):
                    for j in range(borrowList.toDateTime+2):
                        tomorrowTime[j] -= int(count)
                    for j in range(borrowList.fromDateTime,24,1):
                        todayTime[j] -= int(count)
                else:
                    for j in range(borrowList.fromDateTime,borrowList.toDateTime+2):
                        todayTime[j] -= int(count)
    # 내일 현황 (내일기준 반납할 사람 + 빌리는 사람)
    tomorrowBorrow = EquipmentBorrow.objects.filter(fromDate=str(int(Eto)+1))
    for borrowList in tomorrowBorrow:
        for equipList in borrowList.equipment.replace("[", "").replace("]", "").replace("'", "").split(","):
            [equip, count] = equipList.split(":")
            equip = equip.strip()
            count = count.strip()
            if(equip == Ename):
                if(borrowList.fromDate == borrowList.toDate):
                    for j in range(borrowList.fromDateTime, borrowList.toDateTime+2):
                        tomorrowTime[j] -= int(count)
    # for borrowList in borrowLists:
    #     for equipList in borrowList.equipment.replace("[", "").replace("]", "").replace("'", "").split(","):
    #         [equip, count] = equipList.split(":")
    #         equip = equip.strip()
    #         count = count.strip()
    #         if(equip == Ename):
    #             for j in range(borrowList.fromDateTime, borrowList.toDateTime+2):
    #                 todayTime[j] -= int(count)
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
        return render(request, '3-borrow/step2.html', {'borrowLists': borrowList, 'fromTime': fromTime, 'fromDate': fromDate, 'toTime': toTime, 'toDate': toDate})


def borrow_finish(request):
    print(request.POST)
    if(request.method == "POST"):
        EquipmentBorrow.objects.create(
            username=Profile.objects.get(username=request.user),
            equipment="".join(request.POST['borrowList']),
            toDate="".join(request.POST['toDate']).replace("-", ""),
            toDateTime=int(("".join(request.POST['toTime']))[:2]),
            fromDate="".join(request.POST['fromDate']).replace("-", ""),
            fromDateTime=int(("".join(request.POST['fromTime']))[:2]),
            group="".join(request.POST['group']),
            phone="".join(request.POST['phone']),
            purpose="".join(request.POST['purpose']),
            auth="".join(request.POST['auth']),
            remark="".join(request.POST['remark']),
            borrowState=0
        )
        return redirect('main')


def studio_step1(request): 
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d').replace("-", "")
    nextDay = (datetime.datetime.now() +datetime.timedelta(1)).strftime('%Y-%m-%d')
    editorialSudio = Studio.objects.filter(studioType="편집실", isExist=True).values('studioType').distinct()
    soundStudio = Studio.objects.filter(studioType="사운드 스튜디오", isExist=True).values('studioType').distinct()
    sbsStudio = Studio.objects.filter(studioType="SBS 스튜디오", isExist=True).values('studioType').distinct()
    otherObject = makeStudio(editorialSudio, nowDate) +makeStudio(soundStudio, nowDate) + makeStudio(sbsStudio, nowDate)

    if (request.method == "POST"):
        selectDate = ''.join(request.POST['selectDate']).replace("-", "")
        year, month, day = ''.join(request.POST['selectDate']).split("-")
        nextDay = (datetime.datetime(int(year), int(month), int(day))+datetime.timedelta(1)).strftime('%Y-%m-%d')
        otherObject = makeStudio(editorialSudio, selectDate) +makeStudio(soundStudio, selectDate) + makeStudio(sbsStudio, selectDate)
        return render(request, '4-studio/step1.html', {"otherObjects": otherObject, "selectDate": selectDate, "calendar": ''.join(request.POST['selectDate']), "now": datetime.datetime.now().strftime('%Y-%m-%d'), "nextDay": nextDay})
    print(otherObject)
    return render(request, '4-studio/step1.html', {"otherObjects": otherObject, "selectDate": nowDate, "calendar": datetime.datetime.now().strftime('%Y-%m-%d'), "now": datetime.datetime.now().strftime('%Y-%m-%d'), "nextDay": nextDay})

def makeStudio(lists, selectDate):
    resultObject = []
    for studioType in lists:
        studioTypeList = Studio.objects.filter(studioType=studioType['studioType']).values('studioName').distinct()
        resultObject.append(findStudioName(studioTypeList, studioType['studioType'], selectDate))
    return resultObject


def findStudioName(studios, semiType, selectDate):
    totalStudio= []
    for studio in studios:
        totalStudio.append(
            makeStudioDict((studio['studioName']), semiType, selectDate))
    result = {"type": semiType, "info": totalStudio}
    return result


def makeStudioDict(Ename, semiType, selectDate):
    dictEquip = {}
    equipList = Studio.objects.filter(isExist=True, studioName=Ename)
    dictEquip["name"] = Ename
    dictEquip["count"] = len(equipList)
    dictEquip["time1"], dictEquip["time2"] = findStudioTime(
        Ename, selectDate, len(equipList))
    return dictEquip


def findStudioTime(Ename, Eto, Ecount):
    todayTime = [Ecount for i in range(25)]
    tomorrowTime = [Ecount for i in range(25)]
    # 오늘 현황 (오늘 반납할 사람 + 빌리는 사람)
    todayReturn = StudioBorrow.objects.filter(fromDate=str(int(Eto)-1),toDate=Eto)
    todayBorrow = StudioBorrow.objects.filter(fromDate=Eto)
    # 어제 빌림 -> 오늘 반납
    for borrowList in todayReturn:
        for equipList in borrowList.studio.replace("[", "").replace("]", "").replace("'", "").split(","):
            equipList = equipList.strip()
            if(equipList == Ename):
                for j in range(borrowList.toDateTime+2):
                    todayTime[j] -= 1
    # 오늘 빌림
    for borrowList in todayBorrow:
        for equipList in borrowList.studio.replace("[", "").replace("]", "").replace("'", "").split(","):
            equipList = equipList.strip()
            if(equipList == Ename):
                # 내일 반납
                if(int(borrowList.fromDate) < int(borrowList.toDate)):
                    for j in range(borrowList.toDateTime+2):
                        tomorrowTime[j] -= 1
                    for j in range(borrowList.fromDateTime,25,1):
                        todayTime[j] -= 1
                # 오늘 반납
                else:
                    for j in range(borrowList.fromDateTime,borrowList.toDateTime+2):
                        todayTime[j] -= 1
    # 내일 현황 (내일기준 빌리는사람)
    tomorrowBorrow = StudioBorrow.objects.filter(fromDate=str(int(Eto)+1))
    for borrowList in tomorrowBorrow:
        for equipList in borrowList.studio.replace("[", "").replace("]", "").replace("'", "").split(","):
            equipList = equipList.strip()
            if(equipList == Ename):
                if(borrowList.fromDate == borrowList.toDate):
                    for j in range(borrowList.fromDateTime, borrowList.toDateTime+2):
                        tomorrowTime[j] -= 1
    return todayTime, tomorrowTime

def studio_step2(request):
    print(request.POST)
    if(request.method == "POST"):
        borrowList = "".join(request.POST['resultBorrow']).split("//")
        borrowList.pop()
        fromTime = "".join(request.POST['fromTime'])
        toTime = "".join(request.POST['toTime'])
        fromDate = "".join(request.POST['fromDate'])
        toDate = "".join(request.POST['toDate'])
        return render(request, '4-studio/step2.html', {'borrowLists': borrowList, 'fromTime': fromTime, 'fromDate': fromDate, 'toTime': toTime, 'toDate': toDate})


def studio_finish(request):
    print(request.POST)
    if(request.method == "POST"):
        StudioBorrow.objects.create(
            username=Profile.objects.get(username=request.user),
            studio="".join(request.POST['borrowList']),
            fromDate="".join(request.POST['fromDate']).replace("-", ""),
            fromDateTime=int(("".join(request.POST['fromTime']))[:2]),
            toDate="".join(request.POST['toDate']).replace("-", ""),
            toDateTime=int(("".join(request.POST['toTime']))[:2]),
            group="".join(request.POST['group']),
            phone="".join(request.POST['phone']),
            purpose="".join(request.POST['purpose']),
            auth="".join(request.POST['auth']),
            remark="".join(request.POST['remark']),
            studioState=0
        )
        return redirect('main')