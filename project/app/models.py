from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=20, null=True)
    major = models.CharField(max_length=50, null=True)
    penalty = models.IntegerField(null=True)
    # 관리자인 경우 2, 근장인 경우 1, 학생인 경우 0
    isAuth = models.IntegerField(null=True)

    def __str__(self):
        return self.name+'/'+self.major


class Equipment(models.Model):
    equipmentName = models.CharField(max_length=50)
    serialNumber = models.CharField(max_length=50)
    equipType = models.CharField(max_length=50)
    equipSemiType = models.CharField(max_length=50, blank=True, default="")
    # 고장여부
    isExist = models.BooleanField(default=True)
    # 대여가능 0 대여중 1 연체 2
    borrowState = models.IntegerField(default=0)

    def __str__(self):
        return self.equipmentName


class EquipmentBorrow(models.Model):
    username = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='Euser')
    # 장비 -> String처리
    equipment = models.CharField(max_length=200)
    fromDate = models.CharField(max_length=50)
    fromDateTime = models.IntegerField()
    toDate = models.CharField(max_length=50)
    toDateTime = models.IntegerField()
    realDate = models.CharField(max_length=50, default=0)
    realDateTime = models.IntegerField(default=0)
    group = models.CharField(max_length=50, default="")
    purpose = models.CharField(max_length=50, default="")
    auth = models.CharField(max_length=50, default="")
    remark = models.CharField(max_length=50, default="")
    # 대여가능 0 대여중 1 연체 2
    borrowState = models.IntegerField(default=0)

    def __str__(self):
        return f'username={self.username},equipment={self.equipment},fromDate={self.fromDate},fromDateTime={self.fromDateTime},toDate={self.toDate},toDateTime={self.toDateTime},realDate={self.realDate},realDateTime={self.realDateTime},group={self.group},purpose={self.purpose},auth={self.auth},remark={self.remark},borrowState={self.borrowState}'


class Studio(models.Model):
    studioName = models.CharField(max_length=50)
    studioType = models.CharField(max_length=50)
    isExist = models.BooleanField(default=True)

    def __str__(self):
        return self.studioName


class StudioBorrow(models.Model):
    studio = models.ForeignKey(
        Studio, on_delete=models.CASCADE, related_name='Sborrow')
    toDate = models.CharField(max_length=50)
    toDateTime = models.CharField(max_length=50)
    fromDate = models.CharField(max_length=50)
    fromDateTime = models.CharField(max_length=50)
    realDate = models.CharField(max_length=50, default=0)
    realDateTime = models.CharField(max_length=50, default=0)
    division = models.CharField(max_length=50, default="")
    goal = models.CharField(max_length=50, default="")
    isCard = models.BooleanField(default=False)
    willBorrow = models.CharField(max_length=50, default=False)
    Borrow = models.CharField(max_length=50, default=False)
    Borrowed = models.CharField(max_length=50, default=False)

    def __str__(self):
        return self.studio.studioName
