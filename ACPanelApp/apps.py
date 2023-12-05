from django.apps import AppConfig
# import threading
# import time
# from .scheduler import Scheduler
# from .models import ACinfo, Room
# from serverApp.models import ACrecorddetail


class AcpanelappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ACPanelApp'

    # def ready(self):
    #     # 创建全局的实例
    #     scheduler = Scheduler()
    #     scheduler.add_room('1', 10)
    #     scheduler.add_room('2', 15)
    #     scheduler.add_room('3', 18)
    #     scheduler.add_room('4', 12)
    #     scheduler.add_room('5', 14)

    #     def run_scheduler():
    #         while True:
    #             scheduler.step()
    #             acs = ACinfo.objects.all()
    #             for roomNo in scheduler.rooms.keys():
    #                 if Room.objects.filter(roomNo=roomNo).room_status == 'occupied':
    #                     if roomNo in scheduler.service_queue:
    #                         status = 'running'
    #                     elif roomNo in scheduler.waiting_queue:
    #                         status = 'waiting'
    #                     else:
    #                         status = 'stopped'
    #                     current_temperature = scheduler.rooms[roomNo]['current_temperature']
    #                     target_temperature = scheduler.rooms[roomNo]['target_temperature']
    #                     fee = scheduler.rooms[roomNo]['current_cost']
    #                     speed = scheduler.rooms[roomNo]['fan_speed']
    #                     ac = acs.get(roomNo=roomNo)            
    #                     ac.status = status
    #                     ac.current_temperature = current_temperature
    #                     ac.target_temperature = target_temperature
    #                     ac.fee = fee
    #                     ac.speed = speed
    #                     ac.save()
    #                     ACrecorddetail.objects.create(
    #                         roomNo=Room.objects.get(roomNo=roomNo),
    #                         fee=fee,
    #                         speed=speed,
    #                         target_temperature=target_temperature,
    #                         current_temperature=current_temperature,
    #                         status=status
    #                         )
    #             print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' scheduler step')
    #             time.sleep(20)

    #     # 创建新线程来运行调度器
    #     scheduler_thread = threading.Thread(target=run_scheduler)
    #     scheduler_thread.start()