from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

# Create your views here.
from django.views import View

from apps.users.forms import LoginForm, RegisterForm
from apps.users.models import UserProfile, EmailVerifyRecord
from apps.users.utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            #通过用户名和邮箱查询用户
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            #验证密码是否正确
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUser(View):
    def get(self, request, active_code):
        #在数据库中找到激活链接的随机字符串
        all_code = EmailVerifyRecord.objects.filter(code=active_code)
        if all_code:
            for code in all_code:
                #找到随机字符串对应的邮箱/用户名，将用户的激活状态更改为True
                email = code.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        #用户激活成功，返回到登录页面
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        #利用form返回验证码
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        #使用form判断用户输入是否合法
        register_form = RegisterForm(request.POST)
        #判断输入是否合法以及验证码是否正确，如果正确，则执行以下逻辑
        if register_form.is_valid():
            user_name = request.POST.get('email','')
            password = request.POST.get('password','')
            #将注册信息保存到数据库
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            #使用auth下的make_password方法保存密码的密文至数据库
            user_profile.password = make_password(password)
            user_profile.save()
            #调用发送邮件函数发送注册邮件
            send_register_email(user_name, 'register')
            #注册成功返回登录页面
            return render(request, 'login.html')
        else:
            #输入有误，则返回错误信息至前端页面上
            return render(request, 'register.html', {'register_form':register_form})


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        #使用form判断用户POST输入是否合法
        login_form = LoginForm(request.POST)
        #判断输入是否合法，如果合法执行以下逻辑
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=user_name, password=password)
            #判断用户密码是否正确，如果正确则登录成功返回主页面
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            #如果不正确返回用户名或密码错误信息，并继续留在登录页面
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        #如果输入不合法，返回错误信息
        else:
            return render(request, 'login.html', {'login_form':login_form})

