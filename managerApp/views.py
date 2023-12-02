from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from managerApp.models import  CentralAC
from ACPanelApp.models import ACinfo
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

@login_required
def manager(request):
    if request.method == 'GET':
        if request.user.role == 'acmanager':
            return render(request, 'manager.html')

# def manager_register(request):
#     if request.method == 'POST':
#         form = ManagerForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['manager_username']
#             password = form.cleaned_data['manager_password']
#             try:
#                 user = get_user_model().objects.get(manager_username=username)
#                 return JsonResponse({'message': '用户名已存在'})
#             except get_user_model().DoesNotExist:
#                 user = get_user_model()(
#                     manager_username=username,
#                     manager_password=password
#                 )
#                 user.save()
#                 return redirect('/manager/login/')
#     else:
#         form = ManagerForm()
#     return render(request, 'register.html', {'form': form})

# @csrf_exempt
# def manager_register(request):
#     if request.method == 'POST':
#         data = request.body.decode('utf-8')
#         data = json.loads(data)
#         username = data['username']
#         password = data['password']
#         try:
#             user = Manager.objects.get(manager_username=username)
#             return JsonResponse({'message': '用户名已存在'})
#         except Manager.DoesNotExist:
#             user = Manager(
#                 manager_username=username,
#                 manager_password=password
#             )
#             user.save()
#             return JsonResponse({'message': '注册成功'})
#     else:
#         return JsonResponse({'message': '请求方法错误'})

# def manager_login(request):
#     context = {}
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/manager/')
#         else:
#             context['error'] = '用户名或密码错误'
#     return render(request, 'login.html', context)

# @csrf_exempt
# def manager_login(request):
#     if request.method == 'POST':
#         data = request.body.decode('utf-8')
#         data = json.loads(data)
#         username = data['username']
#         password = data['password']
#         try:
#             user = Manager.objects.get(manager_username=username)
#         except Manager.DoesNotExist:
#             return JsonResponse({'message': '用户名或密码错误'})
#         if user.manager_password == password:
#             # if user.manager_token == '':
#             #     token = str(uuid.uuid4())
#             #     user.manager_token = token
#             #     user.save()
#             return JsonResponse({'message': '登录成功'})
#             # else:
#             #     return JsonResponse({'message': '此账号已登录'})
#         else:
#             return JsonResponse({'message': '用户名或密码错误'})
#     else:
#         return JsonResponse({'message': '请求方法错误'})

# def manager_logout(request):
#     logout(request)
#     return redirect('/manager/')

# @csrf_exempt
# def manager_logout(request):
#     if request.method == 'POST':
#         data = request.body.decode('utf-8')
#         try:
#             data = json.loads(data)
#             username = data['username']
#             try:
#                 user = Manager.objects.get(manager_username=username)
#             except Manager.DoesNotExist:
#                 return JsonResponse({'message': '用户名不存在'})
#             if user.manager_token != '':
#                 user.manager_token = ''
#                 user.save()
#                 return JsonResponse({'message': '退出登录成功'})
#             else:
#                 return JsonResponse({'message': '此账号未登录'})
#         except json.decoder.JSONDecodeError:
#             return JsonResponse({'message': '数据格式错误'})
#     else:
#         return JsonResponse({'message': '请求方法错误'})

@login_required
def manager_get_data(request):
    if request.method == 'GET':
        data = ACinfo.objects.all()
        data = list(data.values())
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'message': '请求方法错误'})
    
# @csrf_exempt
# def change_room_status(request):
#     if request.method == 'POST':
#         data = request.body.decode('utf-8')
#         data = json.loads(data)
#         roomNo = data['room']
#         status = data['status'] 
#         if not roomNo or not status:
#             return JsonResponse({'message': '房间号或状态不能为空'})
#         try:
#             room = Room.objects.get(roomNo=roomNo)
#         except Room.DoesNotExist:
#             return JsonResponse({'message': '房间号不存在'})
#         # 创建一个ChangeRecord对象
#         ACrecorddetail.objects.create(roomNo=room, status=status)
#         # 更新对应的LatestChange对象
#         latest_change, created = ACinfo.objects.get_or_create(roomNo=room)
#         if created:
#             latest_change.status = status
#             latest_change.current_temperature = '30'
#             latest_change.target_temperature = '26'
#             latest_change.speed = '1'
#         else:
#             latest_change.status = status
#         latest_change.save()
#         return JsonResponse({'message': '修改成功'})
#     else:
#         return JsonResponse({'message': '请求方法错误'})

@login_required
def central_AC(request):
    if request.method == 'GET':
        centralAC_info = CentralAC.objects.get()
        mode_map = {
            'cool': '制冷',
            'heat': '制热'
        }
        context = {
            'centralAC_info': centralAC_info,
            'mode': mode_map[centralAC_info.centralAC_mode]
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