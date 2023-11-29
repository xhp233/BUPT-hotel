from django.db import models
from ACPanelApp.models import Room

# Create your models here.      

class CentralAC(models.Model):
    MODE_CHOICES = (
        ('cool', 'cool'),
        ('heat', 'heat'),
    )

    STATUS_CHOICES = (
        ('on', 'on'),
        ('off', 'off'),
    )

    centralAC_mode = models.CharField(max_length=50,default='',choices=MODE_CHOICES) # cool or heat
    centralAC_status = models.CharField(max_length=50,default='',choices=STATUS_CHOICES) # on or off
    max_temperature = models.CharField(max_length=50,default='')
    min_temperature = models.CharField(max_length=50,default='')
    low_speed_fee = models.CharField(max_length=50,default='')
    mid_speed_fee = models.CharField(max_length=50,default='')
    high_speed_fee = models.CharField(max_length=50,default='')
    default_target_temperature = models.CharField(max_length=50,default='')

    class Meta:
        db_table = 'centralAC'