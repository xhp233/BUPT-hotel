from django.db import models

# Create your models here.

class Room(models.Model):
    STATUS_CHOICES = (
        ('empty', 'empty'),
        ('occupied', 'occupied'),
    )

    roomNo = models.CharField(max_length=50,primary_key=True)
    room_status = models.CharField(max_length=50,default='',choices=STATUS_CHOICES)# empty, occupied

    class Meta:
        db_table = 'room'

class ACinfo(models.Model):
    STATUS_CHOICES = (
        ('running', 'running'),
        ('stopped', 'stopped'),
        ('waiting', 'waiting'),
    )

    SPEED_CHOICES = (
        ('low', 'low'),
        ('mid', 'mid'),
        ('high', 'high'),
    )

    roomNo = models.OneToOneField(Room, on_delete=models.CASCADE, primary_key=True)
    status = models.CharField(max_length=50,default='',choices=STATUS_CHOICES)# running, stopped, waiting
    current_temperature = models.CharField(max_length=50,default='')
    target_temperature = models.CharField(max_length=50,default='')
    speed = models.CharField(max_length=50,default='',choices=SPEED_CHOICES)# low, mid, high
    fee = models.CharField(max_length=50,default='')

    class Meta:
        db_table = 'acinfo'