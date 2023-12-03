from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse

class MyLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.role == 'acmanager':
            return redirect('ACmanager')
        elif self.request.user.role == 'manager':
            return redirect('Manager')
        elif self.request.user.role == 'frontdesk':
            return redirect('Front Desk')
        elif self.request.user.role == 'resident':
            return redirect('Resident')
        if self.request.user.is_superuser:
            return redirect('../admin/')
        return response

class MyLogoutView(LogoutView):
    next_page = 'login'
    
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, './register.html', {'form': form})

def hello(request):
    return render(request, './hello.html')

# 调度 上限为3 需要队列结构和调度策略（先来先服务，短作业优先，最高优先权调度，时间片轮转等）

# 运行时计算温度变化与费用

# 统计报表

# 账单详单（在前台界面）

# 开房
from django.http import JsonResponse
from ACPanelApp.models import Room
@login_required # 限制未登录用户访问

def receptionist_view(request):
    if request.method == 'GET':
        ##获取所有房间的数据
        acs = Room.objects.all()
        ##返回给对应的html文件
        return render(request, './receptionist.html', {'acs': acs})
    else:
        return JsonResponse({'message': '请求方法错误'})


from serverApp.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
import random

def open_hotel(request):
    if request.method == 'GET':
        roomNo = request.GET.get('roomNo')
        if roomNo is not None:
            Room_info = Room.objects.get(roomNo=roomNo)
            Room_info.room_status = 'occupied'
            Room_info.save()
            password = random.randint(1000, 9999)
            accout_num=roomNo
            #将账号和密码加入数据库
            user=CustomUser.objects.create(username=str(accout_num).zfill(4),role='resident')
            user.set_password(str(password))
            user.save()
        return render(request, './open_hotel.html', {'roomNo': str(accout_num).zfill(4), 'password': password})
    else:
        return JsonResponse({'message': '请求方法错误'})

from ACPanelApp.models import ACinfo
def close_hotel(request):
    if request.method == 'GET':
        roomNo = request.GET.get('roomNo')
        if roomNo is not None:
            Room_info = Room.objects.get(roomNo=roomNo)
            Room_info.room_status = 'empty'
            Room_info.save()

            #将账号和密码从数据库删除
            CustomUser.objects.filter(username=str(roomNo).zfill(4)).delete()

            #获取需要支付的金额
            acInfo=ACinfo.objects.get(roomNo=roomNo)
            bill=acInfo.fee

        return render(request, './close_hotel.html', {'roomNo': roomNo, 'bill': bill})
    else:
        return JsonResponse({'message': '请求方法错误'})

from serverApp.models import ACrecorddetail
def bill(request):
    if request.method == 'GET':
        roomNo = request.GET.get('roomNo')
        if roomNo is not None:
            bill_Info=ACrecorddetail.objects.get(roomNo=roomNo)
            return render(request, './bill.html', {'bill_Info': bill_Info})
    else:
        return JsonResponse({'message': '请求方法错误'})

