"""BUPTHotelAC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from managerApp import views as manager_views
from serverApp import views as server_views


urlpatterns = [
    path('', server_views.hello, name='hello'),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', server_views.MyLoginView.as_view(), name='login'),
    path('logout/', server_views.MyLogoutView.as_view(), name='logout'),
    path('register/', server_views.register_view, name='register'),
    path('manager/', manager_views.manager, name='ACmanager'),

    path('receptionist/', server_views.receptionist_view, name='receptionist'),#添加URL模式
    path('receptionist/open_hotel/',server_views.open_hotel,name='open_hotel'),
    path('receptionist/close_hotel/', server_views.close_hotel, name='close_hotel'),
    path('receptionist/close_hotel/bill/', server_views.bill, name='bill'),

    path('manager/data/', manager_views.manager_get_data),
    path('manager/centralAC/open/', manager_views.open_central_AC),
    path('manager/centralAC/close/', manager_views.close_central_AC),
    path('manager/centralAC/', manager_views.central_AC),
]
