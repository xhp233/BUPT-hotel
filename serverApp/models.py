from django.db import models
from ACPanelApp.models import Room
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('receptionist', 'receptionist'),
        ('acmanager', 'acmanager'),
        ('manager', 'manager'),
        ('resident', 'resident'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        db_table = 'customuser'

# 详单
class ACrecorddetail(models.Model):
    STATUS_CHOICES = (
        ('running', '运行中'),
        ('stopped', '已停止'),
        ('waiting', '等待中'),
    )

    SPEED_CHOICES = (
        ('low', '低'),
        ('mid', '中'),
        ('high', '高'),
    )

    roomNo = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,default='',choices=STATUS_CHOICES)# running, stopped, waiting
    current_temperature = models.CharField(max_length=50,default='')
    target_temperature = models.CharField(max_length=50,default='')
    speed = models.CharField(max_length=50,default='',choices=SPEED_CHOICES)# low, mid, high
    time = models.DateTimeField(auto_now=True)
    fee = models.CharField(max_length=50,default='')

    class Meta:
        db_table = 'ac_record_detail'

# 账单