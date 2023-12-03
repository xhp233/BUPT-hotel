"""
WSGI config for BUPTHotelAC project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
import threading
import time
import os

from django.core.wsgi import get_wsgi_application
from managerApp.models import CentralAC, Room
from ACPanelApp.models import ACinfo
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
    # 删除所有ACadmin对象
    CustomUser.objects.filter(role='acmanager').delete()
    user = CustomUser.objects.create(username='ACadmin', role='acmanager')
    user.set_password('ACadmin')
    user.save()
    print('create ACadmin success')
    return

def create_room(num_of_rooms):
    try:
        # 删除所有Room对象
        Room.objects.all().delete()
    finally:
        pass
    try:        
        Room.objects.create(roomNo=1, room_status='empty')
        for i in range(2, num_of_rooms + 1):
            Room.objects.create(roomNo=i, room_status='occupied')
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

SPEED_TEMP_MAP = {
    'low': 1/3,
    'mid': 1/2,
    'high': 1
}

# 开一个线程，每十秒检查所有空调状态，并以此改变温度
def change_temperature(rooms, acs, mode, status):
    '''
    rooms: Room.objects.all()

    acs: ACinfo.objects.all()

    mode(centralAC): 'heat' or 'cool'

    status(centralAC): 'on' or 'off'
    '''
    if status == 'off':
        return
    if mode == 'heat':
        diff = 1
    elif mode == 'cool':
        diff = -1
    else:
        return
    for room in rooms:
        if room.room_status == 'occupied':
            ac = acs.get(roomNo=room.roomNo)
            current_temperature = float(ac.current_temperature)
            if ac.status == 'running':                
                target_temperature = float(ac.target_temperature)
                if current_temperature == target_temperature:
                    continue
                speed = SPEED_TEMP_MAP[ac.speed] * diff # 温度变化量
                current_temperature += speed
                ac.fee = str(float(ac.fee) + min(abs(speed), abs(current_temperature - target_temperature)))
                if speed > 0: # heat                    
                    if current_temperature >= target_temperature:
                        current_temperature = target_temperature
                else: # cool
                    if current_temperature <= target_temperature:
                        current_temperature = target_temperature
                ac.current_temperature = str(current_temperature)
                ac.save()
            elif ac.status == 'stopped':
                current_temperature -= diff * 0.5 #回温
                ac.current_temperature = str(current_temperature)
                ac.save()
    return

def check_temperature():
    while True:
        print('check temperature')
        time.sleep(3)
        centralAC = CentralAC.objects.get()
        rooms = Room.objects.all()
        acs = ACinfo.objects.all()
        change_temperature(rooms, acs, centralAC.centralAC_mode, centralAC.centralAC_status)

num_of_rooms = 5
create_central_AC()
create_admin()
create_ACadmin()
create_room(num_of_rooms)
# init_AC_info(num_of_rooms)
try:
    ACinfo.objects.all().delete()
finally:
    pass
room = Room.objects.get(roomNo=1)
ACinfo.objects.create(roomNo=room, status='stopped')
room = Room.objects.get(roomNo=2)
ACinfo.objects.create(roomNo=room, status='running', current_temperature='20.0', target_temperature='25.0', speed='low', fee='0')
room = Room.objects.get(roomNo=3)
ACinfo.objects.create(roomNo=room, status='running', current_temperature='10.0', target_temperature='25.0', speed='mid', fee='0')
room = Room.objects.get(roomNo=4)
ACinfo.objects.create(roomNo=room, status='running', current_temperature='0.0', target_temperature='25.0', speed='high', fee='0')
room = Room.objects.get(roomNo=5)
ACinfo.objects.create(roomNo=room, status='running', current_temperature='25.0', target_temperature='30.0', speed='low', fee='0')
print("\nServer activate success\n")
t = threading.Thread(target=check_temperature)
t.start()