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
    if request.method == 'GET':
        # param = request.GET.get('param')
        centralAC_info = CentralAC.objects.get()
        context = {
            'centralAC_info': centralAC_info,
            'mode': centralAC_info.get_centralAC_mode_display(),
            'status': centralAC_info.get_centralAC_status_display(),
            # 'param': param
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