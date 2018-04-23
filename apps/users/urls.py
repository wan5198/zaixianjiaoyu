"""zxjy2018 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from apps.users import views
urlpatterns = [
    path('', views.index,name='users_index'),
    path('login/', views.LoginView.as_view(),name='login'),
    path('logout/', views.logouts,name='logout'),
    path('register/', views.RegView.as_view(),name='register'),#注册
    path('jihuo/<jihuo_code>/', views.JihuoUserView.as_view(),name='jihuo'),#邮箱激活用户
    path('forgetpwd/', views.ForgPwdView.as_view(),name='forgetpwd'),#忘记密码
    path('reset/<active_code>', views.ResetView.as_view(),name='reset_pwd'),#邮箱验证找回密码
    path('modify_pwd/', views.ModifyPwdView.as_view(), name='modify_pwd'),#修改密码
]
