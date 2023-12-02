"""
WSGI config for BUPTHotelAC project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from managerApp.models import CentralAC, Room
from ACPanelApp.models import ACinfo
from django.contrib.auth import authenticate, login, logout, get_user_model
from serverApp.models import CustomUser


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BUPTHotelAC.settings')

application = get_wsgi_application()

def create_central_AC():
    try:
        central_AC = CentralAC.objects.get()
        print('central AC already exists')
    except CentralAC.DoesNotExist:
        # 创建一个CentralAC对象
        CentralAC.objects.create(
            centralAC_mode='cool',
            centralAC_status='off',
            max_temperature='30',
            min_temperature='18',
            speed_fee='1',
            default_target_temperature='25'
        )
        print('create central AC success')

def create_admin():
    if not CustomUser.objects.filter(is_superuser=True).exists():
        CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print('create admin success')
        return
    print('admin already exists')

def create_ACadmin():
    if not CustomUser.objects.filter(role='acmanager').exists():
        user = CustomUser.objects.create(username='ACadmin', role='acmanager')
        user.set_password('ACadmin')
        user.save()
        print('create ACadmin success')
        return
    print('ACadmin already exists')

def create_room(num_of_rooms):
    try:
        # 删除所有Room对象
        Room.objects.all().delete()
    finally:
        pass
    try:        
        for i in range(1, num_of_rooms + 1):
            Room.objects.create(roomNo=i, room_status='empty')
        print('create rooms success')
    except:
        print('rooms already exists')
    
def init_AC_info(num_of_rooms):
    try:
        # 删除所有ACinfo对象
        ACinfo.objects.all().delete()
    finally:
        pass
    try:  
        for i in range(1, num_of_rooms + 1):
            room = Room.objects.get(roomNo=i)
            ACinfo.objects.create(roomNo=room, status='stopped')
        print('create AC info success')
    except:
        print('AC info already exists')

num_of_rooms = 5
create_central_AC()
create_admin()
create_ACadmin()
create_room(num_of_rooms)
init_AC_info(num_of_rooms)
print("\nServer activate success\n")