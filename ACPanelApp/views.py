from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ACinfo, Room
from managerApp.models import CentralAC
from serverApp.models import ACrecorddetail
from django.http import HttpResponse
from BUPTHotelAC.wsgi import scheduler

@login_required # 限制未登录用户访问
def controls(request, room_no):
    ac_info = ACinfo.objects.get(roomNo=room_no)
    centralAC = CentralAC.objects.get()
    context = {
        'room_no': room_no,
        'target_temperature': ac_info.target_temperature,
        'current_temperature': ac_info.current_temperature,
        'speed': ac_info.get_speed_display(),
        'fee': ac_info.fee,
        'status': ac_info.get_status_display(),
        'centralACstatus': centralAC.status,
        'max_temperature': centralAC.max_temperature,
        'min_temperature': centralAC.min_temperature,
        }
    return render(request, 'controls.html', context)

# 开机
def power_on(request, room_no):
    if CentralAC.objects.get().status == 'on':
        scheduler.start_air_conditioning(room_no)
        # ac_info = ACinfo.objects.get(roomNo=room_no)
        # ac_info.status = 'running'
        # ac_info.target_temperature = '22'
        # ac_info.speed = 'mid'
        # ac_info.save()
        # ACrecorddetail.objects.create(
        #     roomNo=Room.objects.get(roomNo=room_no),
        #     fee=0,
        #     speed='mid',
        #     target_temperature='22',
        #     current_temperature=ac_info.current_temperature,
        #     status='running'
        #     )
    return redirect('controls', room_no=room_no)

# 关机
def power_off(request, room_no):
    scheduler.stop_air_conditioning(room_no)
    # ac_info = ACinfo.objects.get(roomNo=room_no)
    # ac_info.status = 'stopped'
    # ac_info.target_temperature = ''
    # ac_info.speed = ''
    # ac_info.save()
    # ACrecorddetail.objects.create(
    #     roomNo=Room.objects.get(roomNo=room_no),
    #     fee=ac_info.fee,
    #     speed='',
    #     target_temperature='',
    #     current_temperature=ac_info.current_temperature,
    #     status='stopped')
    return redirect('controls', room_no=room_no)

# 调温
def adjust_temperature(request, room_no):
    scheduler.set_target_temperature(room_no, int(request.POST.get('target_temp')))
    # ac_info = ACinfo.objects.get(roomNo=room_no)
    # target_temp = request.POST.get('target_temp')
    # if target_temp > CentralAC.objects.get().max_temperature or target_temp < CentralAC.objects.get().min_temperature:
    #     return HttpResponse('Invalid temperature.')    
    # ac_info.target_temperature = target_temp
    # ac_info.save()
    # ACrecorddetail.objects.create(
    #     roomNo=Room.objects.get(roomNo=room_no),
    #     fee=ac_info.fee,
    #     speed=ac_info.speed,
    #     target_temperature=target_temp,
    #     current_temperature=ac_info.current_temperature,
    #     status=ac_info.status)
    return redirect('controls', room_no=room_no)

# 调风速
def adjust_speed(request, room_no):
    scheduler.set_fan_speed(room_no, request.POST.get('speed'))
    # speed = request.POST.get('speed')
    # ac_info = ACinfo.objects.get(roomNo=room_no)
    # ac_info.speed = speed
    # ac_info.save()
    # ACrecorddetail.objects.create(
    #     roomNo=Room.objects.get(roomNo=room_no),
    #     fee=ac_info.fee,
    #     speed=speed,
    #     target_temperature=ac_info.target_temperature,
    #     current_temperature=ac_info.current_temperature,
    #     status=ac_info.status)
    return redirect('controls', room_no=room_no)

# # 温度控制
# def temperature_control(request, room_no):
#     ac_info = ACinfo.objects.get(roomNo=room_no)

#     accumulated_temperature_change = 0
#     target_temperature = float(ac_info.target_temperature)
#     time_interval = 60
#     control_time = 60 * 10
#     start_time = time.time()

#     while time.time() - start_time < control_time:
#         time.sleep(time_interval)
#         current_temperature = float(ac_info.current_temperature)
#         current_temperature += 0.5
#         accumulated_temperature_change += 0.5
#         ac_info.current_temperature = str(current_temperature)
#         ac_info.save()

#         if accumulated_temperature_change >= 1:
#             send_scheduling_request(room_no, 'temperature_control')  # 发送调度请求
#             return HttpResponse(f'Temperature control logic for room {room_no}. Request sent.')

#     return redirect('controls', room_no=room_no)
