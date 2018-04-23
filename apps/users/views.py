from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,reverse,redirect
from django.views.generic.base import View
#增加邮箱也可登陆的功能导入以下3个
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from apps.utils.email_send import send_register_eamil

from .forms import LoginForm,RegForm,ForgetPwdFprm,ModifyPwdForm



# Create your views here.
def index(request):
    return render(request,'index.html')


class LoginView(View):
    def get(self, request):

        return render(request,'login.html')
    def post(self,request):
        login_form =LoginForm(request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            user = authenticate(username=username, password=password) #放进去验证
            if user.is_active: #用户状态为T才可以登录
                login(request,user)
                return render(request,'index.html')
            else:
                context={
                    'msg':'用户名或密码错误！',
                    'login_form':login_form
                }
                return render(request,'login.html',context)
        else:
            context = {

                'login_form': login_form
            }
            return render(request, 'login.html', context)

#让邮箱也可登陆
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None

#登出
def logouts(request):
    logout(request)
    return redirect(reverse('login'))

#注册视图
class RegView(View):
    def get(self,request):
        reg_form = RegForm()
        return render(request,'register.html',{'reg_form':reg_form})
    def post(self,request):
        reg_form =RegForm(request.POST)
        if reg_form.is_valid():
            email = reg_form.cleaned_data['email']
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'reg_form':reg_form,'msg': '邮箱已存在'})
            pass_word = reg_form.cleaned_data['password']
            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.is_active = False
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_eamil(email, 'register')  #调用发送邮件函数，传递给其参数，然后就有该函数发送邮件过去
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'reg_form': reg_form})

#用户邮件激活用户账号
class JihuoUserView(View):
    def get(self, request, jihuo_code): #前端传来这个变量，使用GET方式传递来，接收到
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code = jihuo_code)

        if all_record: #若存在就遍历出来
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email  #把邮箱取出来
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True #将状态改为T，默认是F
                user.save()
         # 验证码不对的时候跳转到激活失败页面
        else:
            return render(request,'jihuoshibai.html')
        # 激活成功跳转到登录页面
        return render(request, "login.html")

#忘记密码发送验证邮件处理视图
class ForgPwdView(View):
    def get(self,request):
        forget_form=ForgetPwdFprm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self, request):
        forget_form = ForgetPwdFprm(request.POST)
        if forget_form.is_valid():
            email = forget_form.cleaned_data['email']
            send_register_eamil(email, 'forget') # 将用户输入的邮件地址和后台标准传入，这里传入'forget'，就发送找回邮
            return render(request, 'pwdzhaohuichenggong.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


#收到验证邮件后，点击邮件链接到这里来处理验证链接传来的信息是否正确，若正确就跳到修改页面
class ResetView(View):
    def get(self, request, active_code): #通过GET方式获取参数
        all_records = EmailVerifyRecord.objects.filter(code=active_code) #将获取的参数（验证码）放到邮件表与记录的验证码核对
        if all_records:
            for record in all_records:
                email = record.email #将该验证码匹配的数据的邮箱取出来
                return render(request, "password_reset.html", {"email":email}) #传递邮箱并跳转到修改密码页面
        else:
            return render(request, "jihuoshibai.html") #失败页面去
        return render(request, "login.html") #回到登录页

#密码修改页面
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = modify_form.cleaned_data['password1']
            pwd2 = modify_form.cleaned_data['password2']
            email = modify_form.cleaned_data['email']
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = modify_form.cleaned_data['email']
            return render(request, "password_reset.html", {"email":email, "modify_form":modify_form })