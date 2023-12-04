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
from managerApp.models import CentralAC
from ACPanelApp.models import ACinfo, Room
from serverApp.models import CustomUser, ACrecorddetail
from .scheduler import Scheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BUPTHotelAC.settings')

application = get_wsgi_application()

def create_central_AC():
    try:
        CentralAC.objects.all().delete()
    finally:
        # 创建一个CentralAC对象
        CentralAC.objects.create(
            mode='',
            status='off',
            max_temperature='',
            min_temperature='',
            fee='',
            default_target_temperature=''
        )
        print('create central AC success')

def create_admin(username='admin', password='admin'):
    if not CustomUser.objects.filter(is_superuser=True).exists():
        CustomUser.objects.create_superuser(username, 'admin@example.com', password)
        print('create admin success')
        return
    print('admin already exists')

def create_ACadmin(username, password):
    # 删除所有ACadmin对象
    CustomUser.objects.filter(role='acmanager').delete()
    user = CustomUser.objects.create(username=username, role='acmanager')
    user.set_password(password)
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
        for i in range(1, num_of_rooms + 1):
            room = Room.objects.get(roomNo=i)
            ACinfo.objects.create(roomNo=room, status='stopped')
        print('create AC info success')

#创建前台服务员：receptionist
def create_receptionist(username, password):
    CustomUser.objects.filter(role='receptionist').delete()
    user = CustomUser.objects.create(username=username, role='receptionist')
    user.set_password(password)
    user.save()
    print('create receptionist success')

def create_ACrecorddetail(num_of_rooms):
    try:
        # 删除所有ACinfo对象
        ACrecorddetail.objects.all().delete()
    finally:
        pass
    try:  
        for i in range(1, num_of_rooms + 1):
            room = Room.objects.get(roomNo=i)
            ACrecorddetail.objects.create(roomNo=room, status='stopped')
        print('create AC record detail success')
    except:
        print('AC record detail already exists')

def delete_all_user():
    try:
        CustomUser.objects.all().delete()
    finally:
        print('delete all user success')

num_of_rooms = 5
create_central_AC()
delete_all_user()
create_admin('admin', 'admin')
create_ACadmin('ACadmin', 'ACadmin')
create_receptionist('receptionist', 'receptionist')
# create_room(num_of_rooms)
# init_AC_info(num_of_rooms)
try:
    ACinfo.objects.all().delete()
finally:
    room = Room.objects.create(roomNo='1', room_status='empty')
    ACinfo.objects.create(roomNo=room, status='stopped', current_temperature='10', fee='0')
    room = Room.objects.create(roomNo='2', room_status='empty')
    ACinfo.objects.create(roomNo=room, status='stopped', current_temperature='15', fee='0')
    room = Room.objects.create(roomNo='3', room_status='empty')
    ACinfo.objects.create(roomNo=room, status='stopped', current_temperature='18', fee='0')
    room = Room.objects.create(roomNo='4', room_status='empty')
    ACinfo.objects.create(roomNo=room, status='stopped', current_temperature='12', fee='0')
    room = Room.objects.create(roomNo='5', room_status='empty')
    ACinfo.objects.create(roomNo=room, status='stopped', current_temperature='14', fee='0')
    print('create AC info success')
print("\nServer activate success\n")

scheduler = Scheduler()
scheduler.add_room('1', 10)
scheduler.add_room('2', 15)
scheduler.add_room('3', 18)
scheduler.add_room('4', 12)
scheduler.add_room('5', 14)

def run_scheduler():
    while True:
        scheduler.step()
        acs = ACinfo.objects.all()
        for roomNo in scheduler.rooms.keys():
            if roomNo in scheduler.service_queue:
                status = 'running'
            elif roomNo in scheduler.waiting_queue:
                status = 'waiting'
            else:
                status = 'stopped'
            current_temperature = scheduler.rooms[roomNo]['current_temperature']
            target_temperature = scheduler.rooms[roomNo]['target_temperature']
            fee = scheduler.rooms[roomNo]['current_cost']
            speed = scheduler.rooms[roomNo]['fan_speed']
            ac = acs.get(roomNo=roomNo)            
            ac.status = status
            ac.current_temperature = current_temperature
            ac.target_temperature = target_temperature
            ac.fee = fee
            ac.speed = speed
            ac.save()
            ACrecorddetail.objects.create(
                roomNo=Room.objects.get(roomNo=roomNo),
                fee=fee,
                speed=speed,
                target_temperature=target_temperature,
                current_temperature=current_temperature,
                status=status
                )

        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' scheduler step')
        time.sleep(20)

# 创建新线程来运行调度器
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()