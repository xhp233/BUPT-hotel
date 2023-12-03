from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from managerApp.models import CentralAC
from ACPanelApp.models import ACinfo
from django.shortcuts import render, redirect

@login_required
def manager(request):
    if request.method == 'GET':
        if request.user.role == 'acmanager':
            return render(request, 'manager.html')

@login_required
def manager_get_data(request):
    if request.method == 'GET':
        data = ACinfo.objects.all()
        data = list(data.values())
        # 将温度费用保留两位小数
        for item in data:
            try:
                item['current_temperature'] = round(float(item['current_temperature']), 2)
                item['target_temperature'] = round(float(item['target_temperature']), 2)
                item['fee'] = round(float(item['fee']), 2)
            except:
                pass
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'message': '请求方法错误'})

@login_required
def central_AC(request):
    if request.method == 'GET':
        centralAC_info = CentralAC.objects.get()
        mode_map = {
            'cool': '制冷',
            'heat': '制热'
        }
        status_map = {
            'on': '开启',
            'off': '关闭'
        }
        context = {
            'centralAC_info': centralAC_info,
            'mode': mode_map[centralAC_info.centralAC_mode],
            'status': status_map[centralAC_info.centralAC_status]
        }
        return render(request, 'central_AC.html', context)
    else:
        return JsonResponse({'message': '请求方法错误'})
    
@login_required
def open_central_AC(request):
    if request.method == 'POST':
        mode = request.POST.get('mode')
        max_temperature = request.POST.get('max_temperature')
        min_temperature = request.POST.get('min_temperature')
        speed_fee = request.POST.get('speed_fee')
        centralAC_info = CentralAC.objects.get()
        centralAC_info.centralAC_status = 'on'
        centralAC_info.centralAC_mode = mode
        centralAC_info.max_temperature = max_temperature
        centralAC_info.min_temperature = min_temperature
        centralAC_info.speed_fee = speed_fee
        centralAC_info.save()

        return redirect('/manager/centralAC/')
    else:
        return JsonResponse({'message': '请求方法错误'})

@login_required
def close_central_AC(request):
    if request.method == 'POST':
        central_AC = CentralAC.objects.get()
        if central_AC.centralAC_status == 'off':
            return JsonResponse({'message': '中央空调未开启'})
        central_AC.centralAC_status = 'off'
        central_AC.save()
        acs = ACinfo.objects.all()
        for ac in acs:
            ac.status = 'stopped'
            ac.target_temperature = ''
            ac.speed = ''
            ac.save()
        return redirect('/manager/centralAC/')
    else:
        return JsonResponse({'message': '请求方法错误'})