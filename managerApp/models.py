from django.db import models    

class CentralAC(models.Model):
    MODE_CHOICES = (
        ('cool', '制冷'),
        ('heat', '制热'),
    )

    STATUS_CHOICES = (
        ('on', '开启'),
        ('off', '关闭'),
    )

    mode = models.CharField(max_length=50,default='',choices=MODE_CHOICES)
    status = models.CharField(max_length=50,default='',choices=STATUS_CHOICES)
    max_temperature = models.CharField(max_length=50,default='')
    min_temperature = models.CharField(max_length=50,default='')
    fee = models.CharField(max_length=50,default='')
    default_target_temperature = models.CharField(max_length=50,default='')

    class Meta:
        db_table = 'centralAC'