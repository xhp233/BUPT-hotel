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
from managerApp import views as manager_views
from serverApp import views as server_views


urlpatterns = [
    path('', server_views.hello, name='hello'),
    path('admin/', admin.site.urls, name='admin'),
    path('login/', server_views.MyLoginView.as_view(), name='login'),
    path('logout/', server_views.MyLogoutView.as_view(), name='logout'),
    path('register/', server_views.register_view, name='register'),
    path('manager/', manager_views.manager, name='ACmanager'),
    path('manager/data/', manager_views.manager_get_data),
    path('manager/centralAC/open/', manager_views.open_central_AC),
    path('manager/centralAC/close/', manager_views.close_central_AC),
    path('manager/centralAC/', manager_views.central_AC),

    path('controls/<int:room_no>/', ACPanelApp_views.controls, name='controls'),
    path('power_on/<int:room_no>/', ACPanelApp_views.power_on, name='power_on'),
    path('power_off/<int:room_no>/', ACPanelApp_views.power_off, name='power_off'),
    path('adjust_temperature/<int:room_no>/<int:target_temp>/', ACPanelApp_views.adjust_temperature, name='adjust_temperature'),
    path('adjust_speed/<int:room_no>/<str:speed>/', ACPanelApp_views.adjust_speed, name='adjust_speed'),
    path('temperature_control/<int:room_no>/', ACPanelApp_views.temperature_control, name='temperature_control'),

    
]
