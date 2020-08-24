from django.shortcuts import render,redirect
from .models import Profile, Equipment, Studio,EquipmentBorrow,StudioBorrow
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
    camera = Equipment.objects.filter(equipType="camera",isExist=True).values('equipSemiType').distinct()
    subCamera =  Equipment.objects.filter(equipType="subcamera",isExist=True).values('equipType').distinct()
    record =  Equipment.objects.filter(equipType="record",isExist=True).values('equipType').distinct()
    light =  Equipment.objects.filter(equipType="light",isExist=True).values('equipType').distinct()
    etc =  Equipment.objects.filter(equipType="etc",isExist=True).values('equipType').distinct()
    cameraObject = makeDictionary(camera,nowDate,"카메라",True)
    subCameraObject = makeDictionary(subCamera,nowDate,"촬영보조장비",False)
    recordObject = makeDictionary(record,nowDate,"녹음장비",False)
    lightObject = makeDictionary(light,nowDate,"조명장비",False)    
    etcObject = makeDictionary(etc,nowDate,"기타장비",False)
    if (request.method == "POST"):
        selectDate = ''.join(request.POST['date']).replace("-","")
        cameraObject = makeDictionary(camera,selectDate,"카메라",True)
        subCameraObject = makeDictionary(subCamera,selectDate,"촬영보조장비",False)
        recordObject = makeDictionary(record,selectDate,"녹음장비",False)
        lightObject = makeDictionary(light,selectDate,"조명장비",False)    
        etcObject = makeDictionary(etc,selectDate,"기타장비",False)
        return render(request, '3-borrow/step1.html',{"cameraObject":cameraObject,"subCameraObject":subCameraObject,"recordObject":recordObject,"lightObject":lightObject,"etcObject":etcObject,"selectDate": selectDate,"calendar" :''.join(request.POST['date'])})
    ob = cameraObject +subCameraObject +recordObject+ lightObject+ etcObject
    print(cameraObject)
    for i in ob: 
        print("😀",i)
    return render(request, '3-borrow/step1.html',{"cameraObject":cameraObject,"subCameraObject":subCameraObject,"recordObject":recordObject,"lightObject":lightObject,"etcObject":etcObject,"selectDate": nowDate, "calendar" : datetime.datetime.now().strftime('%Y-%m-%d')})

def makeDictionary(lists,selectDate,title,isCamera):
    resultObject = []
    if(isCamera):
        for semiType in lists:
            equipTypeList = Equipment.objects.filter(equipSemiType=semiType['equipSemiType']).values('equipmentName').distinct()
            resultObject.append(findName(equipTypeList,semiType['equipSemiType'],selectDate,title))
    else:
        for equipType in lists:
            equipTypeList = Equipment.objects.filter(equipType=equipType['equipType']).values('equipmentName').distinct()
            resultObject.append(findName(equipTypeList,equipType['equipType'],selectDate,title))
    return resultObject

def findName(equiments,semiType,selectDate,title):
    totalEquip = []
    for equiment in equiments:
        totalEquip.append(makeDict((equiment['equipmentName']),semiType,selectDate,title))
    return totalEquip

def makeDict(Ename,semiType,selectDate,title):
    dictEquip = {}
    equipList = Equipment.objects.filter(isExist=True,equipmentName=Ename)
    dictEquip["title"] = title
    dictEquip["type"] = semiType
    dictEquip["name"] = Ename
    dictEquip["count"] = len(equipList)
    dictEquip["time1"], dictEquip["time2"] = findTime(Ename,selectDate,len(equipList))
    return dictEquip

def findTime(Ename,Eto,Ecount):
    todayTime = [Ecount for i in range(24)]
    tomorrowTime = [Ecount for i in range(24)]
    nowhi = EquipmentBorrow.objects.filter(toDate=Eto)
    for i in nowhi:
        if(i.equipment.equipmentName == Ename):
            for j in range(i.fromDateTime,i.toDateTime+1):
                todayTime[j] -= 1
    nowhi = EquipmentBorrow.objects.filter(toDate=str(int(Eto)+1))
    for i in nowhi:
        if(i.equipment.equipmentName == Ename):
            for j in range(i.fromDateTime,i.toDateTime+1):
                tomorrowTime[j] -= 1
    return todayTime[9:18],tomorrowTime[9:18]

def borrow_step2(request):
    if(request.method =="POST"):
        print(request.POST)
        camera = "".join(request.POST['cam'])
        fromTime = "".join(request.POST['fromTime'])
        toTime = "".join(request.POST['toTime'])
        toDate = "".join(request.POST['toDate'])
        return render(request, '3-borrow/step2.html',{'camera':camera,'fromTime':fromTime,'toTime':toTime, 'toDate':toDate})

def borrow_finish(request):
    if(request.method == "POST"):
        print(request.POST['camera'])
        equipment = Equipment.objects.filter(equipmentName=request.POST['camera']).order_by('equipmentName').first()
        EquipmentBorrow.objects.create(
            equipment = equipment,
            toDate = "".join(request.POST['toDate']),
            toDateTime = int(("".join(request.POST['toTime']))[:2]),
            fromDate = "".join(request.POST['toDate']),
            fromDateTime = int(("".join(request.POST['fromTime']))[:2]),
            group = "".join(request.POST['group']),
            purpose = "".join(request.POST['purpose']),
            auth = "".join(request.POST['auth']),
            willBorrow = True
        )
        return redirect('main')
# 로그인 권한 필요시
# @login_required(login_url='/registration/login')

# registration
"""
def signup(request):
    if(request.method =="POST"): 
        found_user = User.objects.filter(username=request.POST['username'])
        if (len(found_user) >0):
            error = 'username이 이미 존재합니다'
            return render(request, 'registration/signup.html',{'error':error})

        new_user =User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],

        )
        print(new_user.pk)
        UserInfo.objects.create(
            user_id=new_user,
            user_pw=request.POST['password'],
            user_type=request.POST['temp3']
        )
        auth.login(
            request,
            new_user,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        return redirect('home')


    return render(request, 'registration/signup.html')


def login(request):
    if (request.method =="POST"):
        found_user =auth.authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if (found_user is None):
            error = '아이디 또는 비밀번호가 틀렸습니다'
            return render(request, 'registration/login.html',{'error':error})

        auth.login(
            request,
            found_user,
            backend='django.contrib.auth.backends.ModelBackend'
        )

        return redirect(request.GET.get('next', '/'))

    return render(request, 'registration/login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')
"""