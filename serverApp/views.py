from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView

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