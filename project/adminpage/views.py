from django.shortcuts import render, redirect
from app.models import Equipment

# Create your views here.

# TODO: 예약 현황 관리 -> 상태별로 띄워주는 것으로 구현
# TODO: 전체 반납 내역 관리 -> 누가 이걸 작성했는지도 알아야됨
# TODO: 장비 모델 추가 및 삭제 (고장 포함) (장비 모델 crud)
# TODO: 슈퍼 사용자가 근장한테 권한 주는 페이지
# TODO: QRcode 입력해서 대여 장비의 상태 바꾸기


def main(request):
    return render(request, "main.html")


def total(request):
    return render(request, "total.html")


def equipment(request):
    return render(request, "equipment.html")


def qrcheck(request):
    return render(request, "qrcheck.html")


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
                isExist=False,
                borrowState=0
            )
            msg = '정상적으로 제품을 등록하였습니다.'
            return render(request, 'addEquipment.html', {"msg": msg})
        else:
            error = '이미 존재하는 serial number 입니다.'
            return render(request, 'addEquipment.html', {"msg": error})
    return render(request, "addequipment.html")


def deleteEquipment(request, equipment_pk):
    deleteEquipment = Equipment.objects.filter(pk=equipment_pk)
    deleteEquipment.delete()
    return redirect('equipment')
