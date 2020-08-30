from django.shortcuts import render, redirect
from .models import Profile, Equipment, Studio, EquipmentBorrow, StudioBorrow
import datetime
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

from .makeObject import *
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
    try:
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d').replace("-", "")
        nextDay = (now +
                datetime.timedelta(1)).strftime('%Y-%m-%d')
        year,month,day = now.strftime('%Y-%m-%d').split("-")
        camera = Equipment.objects.filter(
            equipType="카메라", isExist=True).values('equipType').distinct()
        subCamera = Equipment.objects.filter(
            equipType="카메라 보조 장치", isExist=True).values('equipType').distinct()
        record = Equipment.objects.filter(
            equipType="녹음 장비", isExist=True).values('equipType').distinct()
        light = Equipment.objects.filter(
            equipType="조명", isExist=True).values('equipType').distinct()
        etc = Equipment.objects.filter(
            equipType="기타 부속", isExist=True).values('equipType').distinct()
        #cameraObject = makeDictionary(camera, nowDate)
        otherObject = ResultObject(camera, nowDate, True) + ResultObject(subCamera, nowDate, True) + ResultObject(
            record, nowDate, True) + ResultObject(light, nowDate, True) + ResultObject(etc, nowDate, True)

        if (request.method == "POST"):
            selectDate = ''.join(request.POST['selectDate']).replace("-", "")
            year, month, day = ''.join(request.POST['selectDate']).split("-")
            nextDay = (datetime.datetime(int(year), int(month), int(
                day))+datetime.timedelta(1)).strftime('%Y-%m-%d')
            #cameraObject = makeDictionary(camera, selectDate)
            otherObject = ResultObject(camera, selectDate, True) + ResultObject(subCamera, selectDate, True) + ResultObject(
                record, selectDate, True) + ResultObject(light, selectDate, True) + ResultObject(etc, selectDate, True)
            return render(request, '3-borrow/step1.html', {"otherObjects": otherObject, "year":year,"month":month,"day":day,"calendar": year+"-"+month+"-"+day, "nextDay": nextDay})
        return render(request, '3-borrow/step1.html', {"otherObjects": otherObject, "year":year,"month":month,"day":day,"calendar": year+"-"+month+"-"+day, "nextDay": nextDay})
    except:
        return redirect('error')

def borrow_step2(request):
    if(request.method == "POST"):
            borrowList = "".join(request.POST['resultBorrow']).split("//")
            borrowList.pop()
            fromTime = "".join(request.POST['fromTime'])
            toTime = "".join(request.POST['toTime'])
            fromDate = "".join(request.POST['fromDate'])
            toDate = "".join(request.POST['toDate'])
            return render(request, '3-borrow/step2.html', {'borrowLists': borrowList, 'fromTime': fromTime, 'fromDate': fromDate, 'toTime': toTime, 'toDate': toDate})
    else:
        return redirect('error')


def borrow_finish(request):
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
        return redirect('mypage')
    else:
        return redirect('error')


def studio_step1(request):
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d').replace("-", "")
    nextDay = (now +
               datetime.timedelta(1)).strftime('%Y-%m-%d')
    year,month,day = now.strftime('%Y-%m-%d').split("-")
    editorialSudio = Studio.objects.filter(
        studioType="편집실", isExist=True).values('studioType').distinct()
    soundStudio = Studio.objects.filter(
        studioType="사운드 스튜디오", isExist=True).values('studioType').distinct()
    sbsStudio = Studio.objects.filter(
        studioType="SBS 스튜디오", isExist=True).values('studioType').distinct()
    otherObject = ResultObject(editorialSudio, nowDate, False) + \
        ResultObject(soundStudio, nowDate, False) + ResultObject(sbsStudio, nowDate, False)

    if (request.method == "POST"):
        selectDate = ''.join(request.POST['selectDate']).replace("-", "")
        year, month, day = ''.join(request.POST['selectDate']).split("-")
        nextDay = (datetime.datetime(int(year), int(month), int(
            day))+datetime.timedelta(1)).strftime('%Y-%m-%d')
        otherObject = ResultObject(editorialSudio, selectDate, False) + ResultObject(
            soundStudio, selectDate, False) + ResultObject(sbsStudio, selectDate, False)
        return render(request, '4-studio/step1.html', {"otherObjects": otherObject, "year":year,"month":month,"day":day,"calendar": year+"-"+month+"-"+day, "nextDay": nextDay})
    return render(request, '4-studio/step1.html', {"otherObjects": otherObject, "year":year,"month":month,"day":day,"calendar": year+"-"+month+"-"+day, "nextDay": nextDay})

def studio_step2(request):
    if(request.method == "POST"):
        borrowList = "".join(request.POST['resultBorrow']).split("//")
        borrowList.pop()
        fromTime = "".join(request.POST['fromTime'])
        toTime = "".join(request.POST['toTime'])
        fromDate = "".join(request.POST['fromDate'])
        toDate = "".join(request.POST['toDate'])
        return render(request, '4-studio/step2.html', {'borrowLists': borrowList, 'fromTime': fromTime, 'fromDate': fromDate, 'toTime': toTime, 'toDate': toDate})
    else:
        return redirect('error')

def studio_finish(request):
    if(request.method == "POST"):
        borrowLists = (request.POST['borrowList']).replace("'","").replace("[","").replace("]","").split(",")
        studio = ""
        for borrowList in borrowLists:
            # 편집실 1번 PC => 1번 PC
            if("편집실" in borrowList):
                studio += borrowList[4:] +"//"
            else:
                studio += borrowList + "//"
        StudioBorrow.objects.create(
            username=Profile.objects.get(username=request.user),
            studio=studio,
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
        return redirect('mypage')
    else:
        return redirect('error')

def mypage(request):
    EquipLists = EquipmentBorrow.objects.filter(username=Profile.objects.get(username=request.user))
    StudioLists = StudioBorrow.objects.filter(username=Profile.objects.get(username=request.user))
    return render(request, '5-mypage/mypage.html',{'EquipLists':EquipLists,'StudioLists':StudioLists})

def error(request):
    return render(request, 'error.html')

def logout(request):
    auth.logout(request)
    return redirect('main')