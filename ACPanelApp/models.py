from django.db import models

# Create your models here.

class Room(models.Model):
    STATUS_CHOICES = (
        ('empty', '空闲'),
        ('occupied', '占用'),
    )

    roomNo = models.CharField(max_length=50,primary_key=True)
    room_status = models.CharField(max_length=50,default='',choices=STATUS_CHOICES)
    open_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'room'

class ACinfo(models.Model):
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

    roomNo = models.OneToOneField(Room, on_delete=models.CASCADE, primary_key=True)
    status = models.CharField(max_length=50,default='',choices=STATUS_CHOICES)
    current_temperature = models.CharField(max_length=50,default='')
    target_temperature = models.CharField(max_length=50,default='')
    speed = models.CharField(max_length=50,default='',choices=SPEED_CHOICES)
    fee = models.CharField(max_length=50,default='')

    class Meta:
        db_table = 'acinfo'