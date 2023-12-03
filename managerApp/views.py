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
        return redirect('/manager/centralAC/')
    else:
        return JsonResponse({'message': '请求方法错误'})