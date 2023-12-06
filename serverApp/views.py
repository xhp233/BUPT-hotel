from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from ACPanelApp.models import Room, ACinfo
from serverApp.models import CustomUser, ACrecorddetail
import random
import time

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
            username = self.request.user.username
            roomNo = username.lstrip('0')
            return redirect('controls', room_no=roomNo)
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
        rooms = Room.objects.all()
        # 将status转换为中文
        for room in rooms:
            room.room_status = room.get_room_status_display()
        ##返回给对应的html文件
        return render(request, './receptionist.html', {'rooms': rooms})
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
            ACrecorddetail.objects.create(roomNo=Room_info)
        return render(request, './open_hotel.html', {'roomNo': str(accout_num).zfill(4), 'password': password})
    else:
        return JsonResponse({'message': '请求方法错误'})

def close_hotel(request):
    if request.method == 'GET':
        roomNo = request.GET.get('roomNo')
        if roomNo is not None:
            # 将房间状态改为空闲
            Room_info = Room.objects.get(roomNo=roomNo)
            Room_info.room_status = 'empty'
            Room_info.save()

            #将账号和密码从数据库删除
            CustomUser.objects.filter(username=str(roomNo).zfill(4)).delete()

            #获取需要支付的金额
            acInfo=ACinfo.objects.get(roomNo=roomNo)
            bill=acInfo.fee

            #将空调信息清空
            acInfo.status='stopped'
            acInfo.target_temperature=''
            acInfo.speed=''
            acInfo.fee=''
            acInfo.save()

            room = Room.objects.get(roomNo=roomNo)

            context = {
                'roomNo': roomNo,
                'bill': bill,
                'startTime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(room.open_time.timestamp())),
                'endTime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
            }

            return render(request, './close_hotel.html', context)
        return JsonResponse({'message': '房间号为空'})
    else:
        return JsonResponse({'message': '请求方法错误'})

def bill(request):
    if request.method == 'GET':
        roomNo = request.GET.get('roomNo')
        bill_Infos=ACrecorddetail.objects.all().filter(roomNo=roomNo)
        # 删除最后创建的一条记录
        bill_Infos.last().delete()
        total_fee = 0
        # 将fee字段由累计费用改为每次消费
        for bill_Info in bill_Infos:
            bill_Info.fee = float(bill_Info.fee) - total_fee
            total_fee += float(bill_Info.fee)
            bill_Info.save()
        # 删除fee为0的记录
        bill_Infos = bill_Infos.exclude(fee=0.0)
        for bill_Info in bill_Infos:
            bill_Info.speed = bill_Info.get_speed_display()
            bill_Info.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(bill_Info.start_time.timestamp()))
            bill_Info.end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(bill_Info.end_time.timestamp()))
            bill_Info.request_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(bill_Info.request_time.timestamp()))
        respose = render(request, './bill.html', {'bill_Infos': bill_Infos, 'total_fee': total_fee})
        #删除数据库中的详单信息
        bill_Infos.delete()
        return respose
    else:
        return JsonResponse({'message': '请求方法错误'})

