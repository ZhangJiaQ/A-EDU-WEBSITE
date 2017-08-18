from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import authenticate, login


# Create your views here.
from django.views import View

from apps.users.forms import LoginForm, RegisterForm
from apps.users.models import UserProfile


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


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            pass


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
                login(request, user)
                return render(request, 'index.html')
            #如果不正确返回用户名或密码错误信息，并继续留在登录页面
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        #如果输入不合法，返回错误信息
        else:
            return render(request, 'login.html', {'login_form':login_form})

