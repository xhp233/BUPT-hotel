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

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        db_table = 'customuser'

# 详单
class ACrecorddetail(models.Model):
    roomNo = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,default='')
    current_temperature = models.CharField(max_length=50,default='')
    target_temperature = models.CharField(max_length=50,default='')
    speed = models.CharField(max_length=50,default='')
    time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ac_record_detail'

# 账单