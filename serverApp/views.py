from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from ACPanelApp.models import Room, ACinfo
from serverApp.models import CustomUser, ACrecorddetail
import random

class MyLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.role == 'acmanager':
            return redirect('ACmanager')
        elif self.request.user.role == 'manager':
            return redirect('Manager')
        elif self.request.user.role == 'receptionist':
            return redirect('receptionist')
        elif self.request.user.role == 'resident':
            return redirect('Resident')
        if self.request.user.is_superuser:
            return redirect('../admin/')
        return response

class MyLogoutView(LogoutView):
    next_page = 'login'

def hello(request):
    return render(request, './hello.html')

@login_required # 限制未登录用户访问
def receptionist_view(request):
    if request.method == 'GET':
        ##获取所有房间的数据
        acs = Room.objects.all()
        # 将status转换为中文
        for ac in acs:
            ac.room_status = ac.get_room_status_display()
        ##返回给对应的html文件
        return render(request, './receptionist.html', {'acs': acs})
    else:
        return JsonResponse({'message': '请求方法错误'})

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

def bill(request):
    if request.method == 'GET':
        roomNo = request.GET.get('roomNo')
        if roomNo is not None:
            bill_Info=ACrecorddetail.objects.get(roomNo=roomNo)
            return render(request, './bill.html', {'bill_Info': bill_Info})
    else:
        return JsonResponse({'message': '请求方法错误'})

