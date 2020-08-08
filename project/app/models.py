from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    # 관리자인 경우 1, 학생인 경우 0
    isAuth = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Equipment(models.Model):
    equipmentName = models.CharField(max_length=50)
    serialNumber = models.CharField(max_length=50)
    equipType = models.CharField(max_length=50)
    isExist = models.BooleanField(default = True)
    def __str__(self):
        return self.equipmentName

class Studio(models.Model):
    studioName = models.CharField(max_length=50)
    studioType = models.CharField(max_length=50)
    isExist = models.BooleanField(default = True)
    def __str__(self):
        return self.studioName

class EquipmentBorrow(models.Model):
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name='Eborrow')
    toDate = models.CharField(max_length=50)
    toDateTime = models.IntegerField(max_length=50)
    fromDate = models.CharField(max_length=50)
    fromDateTime = models.IntegerField(max_length=50)
    realDate = models.CharField(max_length=50, default=0)
    realDateTime = models.IntegerField(max_length=50, default=0)
    group = models.CharField(max_length=50, default = "")
    purpose = models.CharField(max_length=50,default = "")
    auth = models.CharField(max_length=50, default = "")
    remark = models.CharField(max_length=50, default = "")
    willBorrow = models.CharField(max_length=50, default = False)
    Borrow = models.CharField(max_length=50, default = False)
    Borrowed = models.CharField(max_length=50, default = False)

    def __str__(self):
        return self.equipment.equipmentName

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
    goal = models.CharField(max_length=50, default = "")
    isCard = models.BooleanField(default = False)
    willBorrow = models.CharField(max_length=50,default = False)
    Borrow = models.CharField(max_length=50, default = False)
    Borrowed = models.CharField(max_length=50, default = False)

    def __str__(self):
        return self.studio.studioName

