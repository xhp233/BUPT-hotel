from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from managerApp.models import CentralAC
from ACPanelApp.models import ACinfo
from django.shortcuts import render, redirect
from BUPTHotelAC.scheduler import scheduler

@login_required
def manager(request):
    '''
    该函数用于处理管理员界面的请求
    :param request: 请求
    :return: 渲染后的管理员界面
    '''
    if request.user.role != 'acmanager':
        return HttpResponse('您没有权限访问该页面')
    if request.method == 'GET':
        if request.user.role == 'acmanager':
            return render(request, 'manager.html')

@login_required
def manager_get_data(request):
    '''
    该函数用于处理管理员界面的获取数据请求
    :param request: 请求
    :return: json格式的数据
    '''
    if request.user.role != 'acmanager':
        return HttpResponse('您没有权限访问该页面')
    if request.method == 'GET':
        data = ACinfo.objects.all()
        data = list(data.values())
        # 将status转换为中文
        for ac in data:
            ac['status'] = ACinfo.objects.get(roomNo=ac['roomNo_id']).get_status_display()
            ac['speed'] = ACinfo.objects.get(roomNo=ac['roomNo_id']).get_speed_display()
        # 将温度费用保留两位小数
        for ac in data:
            try:
                ac['fee'] = round(float(ac['fee']), 2)
                ac['target_temperature'] = ACinfo.objects.get(roomNo=ac['roomNo_id']).target_temperature
                ac['current_temperature'] = ACinfo.objects.get(roomNo=ac['roomNo_id']).current_temperature
            except:
                pass
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'message': '请求方法错误'})

@login_required
def central_AC(request):
    '''
    该函数用于处理中央空调界面的请求
    :param request: 请求
    :return: 渲染后的中央空调界面
    '''
    if request.user.role != 'acmanager':
        return HttpResponse('您没有权限访问该页面')
    if request.method == 'GET':
        # 获取中央空调的信息
        centralAC_info = CentralAC.objects.get()
        centralAC_info.mode = centralAC_info.get_mode_display()
        centralAC_info.status = centralAC_info.get_status_display()
        return render(request, 'central_AC.html', {'centralAC_info': centralAC_info})
    else:
        return JsonResponse({'message': '请求方法错误'})
    
@login_required
def open_central_AC(request):
    '''
    该函数用于处理开启中央空调的请求
    :param request: 请求
    :return: 重定向到中央空调界面
    '''
    if request.user.role != 'acmanager':
        return HttpResponse('您没有权限访问该页面')
    if request.method == 'POST':
        # 获取中央空调的信息
        mode = request.POST.get('mode')
        max_temperature = request.POST.get('max_temperature')
        min_temperature = request.POST.get('min_temperature')
        fee = request.POST.get('fee')
        default_target_temperature = request.POST.get('default_target_temperature')
        # 将中央空调的信息保存到数据库
        centralAC_info = CentralAC.objects.get()
        centralAC_info.status = 'on'
        centralAC_info.mode = mode
        centralAC_info.max_temperature = max_temperature
        centralAC_info.min_temperature = min_temperature
        centralAC_info.fee = fee
        centralAC_info.default_target_temperature = default_target_temperature
        centralAC_info.save()
        # 同步给调度器
        scheduler.set_params(default_target_temperature, fee, 1.0, 1 if mode == 'heat' else -1)
        return redirect('/manager/centralAC/')
    else:
        return JsonResponse({'message': '请求方法错误'})

@login_required
def close_central_AC(request):
    '''
    该函数用于处理关闭中央空调的请求
    :param request: 请求
    :return: 重定向到中央空调界面
    '''
    if request.user.role != 'acmanager':
        return HttpResponse('您没有权限访问该页面')
    if request.method == 'POST':
        # 获取中央空调的信息
        central_AC = CentralAC.objects.get()
        # 将中央空调的信息保存到数据库
        if central_AC.status == 'off':
            return JsonResponse({'message': '中央空调未开启'})
        central_AC.status = 'off'
        central_AC.save()
        # 关闭所有空调
        acs = ACinfo.objects.all()
        for ac in acs:
            ac.status = 'stopped'
            ac.target_temperature = ''
            ac.speed = ''
            ac.save()
        return redirect('/manager/centralAC/')
    else:
        return JsonResponse({'message': '请求方法错误'})