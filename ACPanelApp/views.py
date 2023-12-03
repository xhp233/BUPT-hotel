from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ACinfo
import requests  # Import the requests library for making HTTP requests
import time


def controls(request, room_no):
    ac_instance = ACinfo.objects.get(roomNo=room_no)
    context = {'room_no': room_no, 'current_temperature': ac_instance.current_temperature}
    return render(request, 'controls.html', context)

# 开机
def power_on(request, room_no):
    ac_instance = ACinfo.objects.get(roomNo=room_no)
    ac_instance.status = 'running'
    ac_instance.save()
    send_scheduling_request(room_no, 'power_on')  # 发送调度请求
    return HttpResponse(f'AC in room {room_no} is powered on.')

# 关机
def power_off(request, room_no):
    ac_instance = ACinfo.objects.get(roomNo=room_no)
    ac_instance.status = 'stopped'
    ac_instance.save()
    send_scheduling_request(room_no, 'power_off')  # 发送调度请求
    return HttpResponse(f'AC in room {room_no} is powered off.')

# 调温
def adjust_temperature(request, room_no, target_temp):
    ac_instance = ACinfo.objects.get(roomNo=room_no)
    ac_instance.target_temperature = target_temp
    ac_instance.save()
    send_scheduling_request(room_no, 'adjust_temperature')  # 发送调度请求
    return HttpResponse(f'Temperature in room {room_no} adjusted to {target_temp}.')

# 调风速
def adjust_speed(request, room_no, speed):
    ac_instance = ACinfo.objects.get(roomNo=room_no)
    ac_instance.speed = speed
    ac_instance.save()
    send_scheduling_request(room_no, 'adjust_speed')  # 发送调度请求
    return HttpResponse(f'AC in room {room_no} speed adjusted to {speed}.')

# 温度控制
def temperature_control(request, room_no):
    ac_instance = ACinfo.objects.get(roomNo=room_no)

    accumulated_temperature_change = 0
    target_temperature = float(ac_instance.target_temperature)
    time_interval = 60
    control_time = 60 * 10
    start_time = time.time()

    while time.time() - start_time < control_time:
        time.sleep(time_interval)
        current_temperature = float(ac_instance.current_temperature)
        current_temperature += 0.5
        accumulated_temperature_change += 0.5
        ac_instance.current_temperature = str(current_temperature)
        ac_instance.save()

        if accumulated_temperature_change >= 1:
            send_scheduling_request(room_no, 'temperature_control')  # 发送调度请求
            return HttpResponse(f'Temperature control logic for room {room_no}. Request sent.')

    return HttpResponse(f'Temperature control logic for room {room_no} completed.')

# 发送调度请求的函数
def send_scheduling_request(room_no, action):
    # 模拟向服务器发送调度请求，实际中需要替换为实际的服务器端点和数据
    server_endpoint = 'http://example.com/schedule'
    payload = {'room_no': room_no, 'action': action}
    response = requests.post(server_endpoint, data=payload)

    # 需要根据服务器的响应进行适当的处理
    if response.status_code == 200:
        print(f'Scheduling request for room {room_no} {action} sent successfully.')
    else:
        print(f'Failed to send scheduling request for room {room_no} {action}.')
