from django.shortcuts import render, redirect
from app.models import Equipment, EquipmentBorrow

# Create your views here.

# TODO: 예약 현황 관리 -> 상태별로 띄워주는 것으로 구현
# TODO: 전체 반납 내역 관리 -> 누가 이걸 작성했는지도 알아야됨
# TODO: 장비 모델 추가 및 삭제 (고장 포함) (장비 모델 crud)
# TODO: 슈퍼 사용자가 근장한테 권한 주는 페이지
# TODO: QRcode 입력해서 대여 장비의 상태 바꾸기


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
    return render(request, "total.html")


def equipment(request):
    # 장비 목록 다 보여주면 됨
    # 장비 추가는 따로 탭을 만들거고
    # 장비 삭제 및 사용 불가 처리는 여기서 할 수 있도록
    # 함수는 따로 뺴야됨
    equipments = Equipment.objects.all()
    return render(request, "equipment.html", {"equipments": equipments})


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
