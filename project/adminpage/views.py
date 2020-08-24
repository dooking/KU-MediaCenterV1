from django.shortcuts import render

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
    return render(request, "addequipment.html")
