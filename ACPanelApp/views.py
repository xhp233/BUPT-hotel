from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ACinfo
from serverApp.models import ACrecorddetail
from managerApp.models import CentralAC
from BUPTHotelAC.scheduler import scheduler
import time

@login_required # 限制未登录用户访问
def controls(request, room_no):
    '''
    该函数用于处理控制界面的请求
    :param request: 请求
    :param room_no: 房间号
    :return: 渲染后的控制界面
    '''
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
        'default_target_temperature': centralAC.default_target_temperature,
        }
    return render(request, 'controls.html', context)

def set_request_time(room_no):
    # 在详单的最后一项中设置请求时间
    ac_record_detail = ACrecorddetail.objects.filter(roomNo=room_no).last()
    ac_record_detail.request_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    ac_record_detail.save()

# 开机
def power_on(request, room_no):
    if ACinfo.objects.get(roomNo=room_no).status == 'stopped':
        if CentralAC.objects.get().status == 'on':
            scheduler.start_air_conditioning(str(room_no))
    return redirect('controls', room_no=room_no)

# 关机
def power_off(request, room_no):
    scheduler.stop_air_conditioning(str(room_no))
    return redirect('controls', room_no=room_no)

# 调温
def adjust_temperature(request, room_no):
    scheduler.set_target_temperature(str(room_no), int(request.POST.get('target_temp')))
    return redirect('controls', room_no=room_no)

# 调风速
def adjust_speed(request, room_no):
    scheduler.set_fan_speed(str(room_no), request.POST.get('speed'))
    return redirect('controls', room_no=room_no)