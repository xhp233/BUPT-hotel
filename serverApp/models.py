from django.db import models
from ACPanelApp.models import Room
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20)
    roomNo = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'customuser'

# 详单
class ACrecorddetail(models.Model):
    SPEED_CHOICES = (
        ('low', '低'),
        ('mid', '中'),
        ('high', '高'),
    )

    roomNo = models.ForeignKey(Room, on_delete=models.CASCADE)
    current_temperature = models.CharField(max_length=50,default='')
    target_temperature = models.CharField(max_length=50,default='')
    speed = models.CharField(max_length=50,default='',choices=SPEED_CHOICES)# low, mid, high
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    request_time = models.DateTimeField(auto_now_add=True)
    fee = models.CharField(max_length=50,default='')
    fee_rate = models.CharField(max_length=50,default='')

    class Meta:
        db_table = 'ac_record_detail'

# 账单
# class ACrecord(models.Model):
#     roomNo = models.ForeignKey(Room, on_delete=models.CASCADE)
#     start_time = models.DateTimeField(auto_now_add=True)
#     end_time = models.DateTimeField(auto_now=True)
#     fee = models.CharField(max_length=50,default='')

#     class Meta:
#         db_table = 'ac_record'