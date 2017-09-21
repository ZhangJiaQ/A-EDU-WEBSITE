from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

# Create your views here.
from django.views import View

from apps.users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, ImageUploadForm
from apps.users.models import UserProfile, EmailVerifyRecord
from apps.users.utils.email_send import send_register_email
from apps.utils.mixin_utils import LoginRequiredMixin


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
                # 用户激活成功，返回到登录页面
                return render(request, 'login.html')
        else:
            return render(request, 'Active_wrong.html')


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
            #验证用户是否已经存在
            if UserProfile.objects.filter(username=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户名已存在'})
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


class ForgetPsd(View):
    def get(self, request):
        #验证用户输入是否合法，如果不合法则返回错误信息，并返回验证码
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form':forgetpwd_form})

    def post(self, request):
        # 验证用户POST是否合法，如果不合法则返回错误信息
        forgetpwd_form = ForgetPwdForm(request.POST)
        #如果输入有效的话，则执行以下逻辑
        if forgetpwd_form.is_valid():
            email = request.POST.get('email')
            #发送密码修改邮件
            send_register_email(email, 'forgetpwd')
            #返回发送成功页面
            return render(request, 'send_sesscufly.html')
        #如果输入有误，则返回忘记密码页面，并返回错误信息和验证码
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form, 'msg':'输入有误'})


class ResetPwd(View):
    #找回密码邮件中的找回密码网址GET方法
    def get(self, request, active_code):
        #在数据库中找到激活链接的随机字符串
        all_code = EmailVerifyRecord.objects.filter(code=active_code)
        if all_code:
            for code in all_code:
                #返回URL对应的所需要修改密码的账号，并嵌入在html内
                email = code.email
                #返回修改密码的网站和对应的账号
                return render(request, 'password_reset.html', {'email':email})
        else:
            return render(request, 'Active_wrong.html')


class ModefyPwd(View):
    #修改密码的网站
    def post(self, request):
        #验证POST是否无误
        modify_pwd = ModifyPwdForm(request.POST)
        if modify_pwd.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            email = request.POST.get('email')
            #判断两次输入密码是否一致
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email':email, 'msg': '两次输入密码不一致'})
            user = UserProfile.objects.get(email=email)
            #修改对应账户密码
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        #如果POST有误，则返回找回密码网站与对应的账号
        else:
            email = request.POST.get('email')
            return render(request, 'password_reset.html', {'email': email})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })


class ImageUploadView(LoginRequiredMixin, View):

    def post(self, request):
        '''
        image_form = ImageUploadForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save
        '''
        image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')