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
            mode='heat',
            status='on',
            max_temperature='30',
            min_temperature='16',
            fee='1',
            default_target_temperature='22'
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
        # 删除
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

use_test_case = False
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
    Room.objects.all().delete()
finally:
    room = Room.objects.create(roomNo='1', room_status='occupied' if use_test_case else 'empty')
    ACinfo.objects.create(roomNo=room, status='stopped', current_temperature='10', fee='0')
    room = Room.objects.create(roomNo='2', room_status='occupied' if use_test_case else 'empty')
    ACinfo.objects.create(roomNo=room, status='stopped', current_temperature='15', fee='0')
    room = Room.objects.create(roomNo='3', room_status='occupied' if use_test_case else 'empty')
    ACinfo.objects.create(roomNo=room, status='stopped', current_temperature='18', fee='0')
    room = Room.objects.create(roomNo='4', room_status='occupied' if use_test_case else 'empty')
    ACinfo.objects.create(roomNo=room, status='stopped', current_temperature='12', fee='0')
    room = Room.objects.create(roomNo='5', room_status='occupied' if use_test_case else 'empty')
    ACinfo.objects.create(roomNo=room, status='stopped', current_temperature='14', fee='0')
    print('create AC info success')
create_ACrecorddetail(num_of_rooms)

print("\nServer activate success\n")

scheduler = Scheduler()
scheduler.add_room('1', 10)
scheduler.add_room('2', 15)
scheduler.add_room('3', 18)
scheduler.add_room('4', 12)
scheduler.add_room('5', 14)

def run_scheduler(wait):
    count = 0
    while True:
        count += 1
        time.sleep(wait)
        scheduler.step()
        acs = ACinfo.objects.all()
        for roomNo in scheduler.rooms.keys():
            room = Room.objects.get(roomNo=roomNo)
            if room.room_status == 'occupied':
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

        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' scheduler step ' + str(count))

wait = 10
# 创建新线程来运行调度器
scheduler_thread = threading.Thread(target=run_scheduler, args=(wait,))
scheduler_thread.start()

def room1(wait):
    time.sleep(3)
    scheduler.start_air_conditioning('1')
    time.sleep(wait)
    scheduler.set_target_temperature('1', 24)
    time.sleep(4*wait)
    scheduler.set_fan_speed('1', 'high')
    time.sleep(4*wait)
    scheduler.set_target_temperature('1', 28)
    time.sleep(5*wait)
    scheduler.stop_air_conditioning('1')
    time.sleep(4*wait)
    scheduler.start_air_conditioning('1')
    time.sleep(6*wait)
    scheduler.stop_air_conditioning('1')

def room2(wait):
    time.sleep(4)
    time.sleep(wait)
    scheduler.start_air_conditioning('2')
    time.sleep(2*wait)
    scheduler.set_target_temperature('2', 25)
    time.sleep(9*wait)
    scheduler.set_fan_speed('2', 'high')
    time.sleep(8*wait)
    scheduler.set_target_temperature('2', 27)
    scheduler.set_fan_speed('2', 'mid')
    time.sleep(5*wait)
    scheduler.stop_air_conditioning('2')

def room3(wait):
    time.sleep(5)
    time.sleep(2*wait)
    scheduler.start_air_conditioning('3')
    time.sleep(2*wait)
    scheduler.set_target_temperature('3', 27)
    time.sleep(10*wait)
    scheduler.set_fan_speed('3', 'low')
    time.sleep(3*wait)
    scheduler.set_fan_speed('3', 'high')
    time.sleep(7*wait)
    scheduler.stop_air_conditioning('3')

def room4(wait):
    time.sleep(6)
    time.sleep(3*wait)
    scheduler.start_air_conditioning('4')
    time.sleep(6*wait)
    scheduler.set_target_temperature('4', 28)
    scheduler.set_fan_speed('4', 'high')
    time.sleep(9*wait)
    scheduler.set_target_temperature('4', 25)
    scheduler.set_fan_speed('4', 'mid')
    time.sleep(7*wait)
    scheduler.stop_air_conditioning('4')

def room5(wait):
    time.sleep(7)
    time.sleep(3*wait)
    scheduler.start_air_conditioning('5')
    time.sleep(wait)
    scheduler.set_fan_speed('5', 'high')
    time.sleep(3*wait)
    scheduler.set_target_temperature('5', 24)
    time.sleep(4*wait)
    scheduler.set_fan_speed('5', 'mid')
    time.sleep(5*wait)
    scheduler.stop_air_conditioning('5')
    time.sleep(4*wait)
    scheduler.start_air_conditioning('5')
    time.sleep(4*wait)
    scheduler.stop_air_conditioning('5')

def test_case():
    room1_thread = threading.Thread(target=room1, args=(wait,))
    room2_thread = threading.Thread(target=room2, args=(wait,))
    room3_thread = threading.Thread(target=room3, args=(wait,))
    room4_thread = threading.Thread(target=room4, args=(wait,))
    room5_thread = threading.Thread(target=room5, args=(wait,))
    room1_thread.start()
    room2_thread.start()
    room3_thread.start()
    room4_thread.start()
    room5_thread.start()

if use_test_case:
    test_case()