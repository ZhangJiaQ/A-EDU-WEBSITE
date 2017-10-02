import json

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse

# Create your views here.
from django.views import View

from apps.course.models import Course
from apps.operation.models import UserCourse, UserFavorite, UserMessage
from apps.organization.models import CourseOrg, Teacher
from apps.users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, ImageUploadForm, UserInfoUpdateForm
from apps.users.models import UserProfile, EmailVerifyRecord, PageBanner
from apps.users.utils.email_send import send_register_email
from apps.utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


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


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


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
                    return HttpResponseRedirect(reverse('login'))
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
        return render(request, 'usercenter-info.html', {})


    def post(self, request):
        #修改个人信息,首先验证信息输入是否合法
        update_info = UserInfoUpdateForm(request.POST, instance=request.user)
        #如果合法，直接提交
        if update_info.is_valid():
            update_info.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(update_info.errors), content_type='application/json')


class ImageUploadView(LoginRequiredMixin, View):

    def post(self, request):
        '''
        image_form = ImageUploadForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save
        '''
        #取出返回的图像
        image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        #验证图像是否正确
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwd(LoginRequiredMixin, View):
    """
        个人中心更新密码
    """
    def post(self, request):
        #验证POST是否无误
        modify_pwd = ModifyPwdForm(request.POST)
        if modify_pwd.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            #判断两次输入密码是否一致
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail"}', content_type='application/json')
            user = request.user
            #修改对应账户密码
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        #如果POST有误，则返回找回密码网站与对应的账号
        else:
            return HttpResponse(json.dumps(modify_pwd.errors), content_type='application/json')


class UpdateEmail(LoginRequiredMixin, View):

    def get(self, request):
        email = request.GET.get('email', '')
        #验证邮箱是否已经存在
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        #发送验证码邮件
        send_register_email(email, 'update')
        return HttpResponse('{"status":"success"}', content_type='application/json')


    def post(self, request):
        #取出相应的字段
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        #判断验证码是否在数据库中（验证码是否正确），如果正确，则修改邮箱，如果不正确，返回错误信息
        if EmailVerifyRecord.objects.filter(email=email, code=code):
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class UserCourseView(LoginRequiredMixin, View):

    def get(self, request):
        user_course = UserCourse.objects.all()
        return render(request, 'usercenter-mycourse.html', {
            'user_course':user_course,
        })


class UserFavOrgView(LoginRequiredMixin, View):

    def get(self, request):
        org_list = []
        fav_ids = UserFavorite.objects.filter(user=request.user, fav_type='3')
        for fav_id in fav_ids:
            org_id = fav_id.id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list':org_list,
        })


class UserFavCourseView(LoginRequiredMixin, View):

    def get(self, request):
        course_list = []
        fav_ids = UserFavorite.objects.filter(user=request.user, fav_type='1')
        for fav_id in fav_ids:
            course_id = fav_id.id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list':course_list,
        })


class UserFavTeacherView(LoginRequiredMixin, View):

    def get(self, request):
        teacher_list = []
        fav_ids = UserFavorite.objects.filter(user=request.user, fav_type='2')
        for fav_id in fav_ids:
            teacher_id = fav_id.id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list':teacher_list,
        })


class UserMessageView(LoginRequiredMixin, View):

    def get(self, request):
        message_list = UserMessage.objects.filter(Q(user=0)|Q(user=request.user.id))

        #消息已读功能
        has_read_messages = UserMessage.objects.filter(Q(user=0)|Q(user=request.user.id), has_read=False)
        for message in has_read_messages:
            message.has_read = True
            message.save()

        # 分页功能的实现
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(message_list, 1, request=request)
        paged_message = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages':paged_message
        })


class IndexView(View):
    def get(self, request):
        #course banner
        #org tag
        bannar_list = PageBanner.objects.all()
        bannar_course = Course.objects.filter(is_bannar=True)
        course_list = Course.objects.all()[:6]
        org_list = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'bannar_list':bannar_list,
            'bannar_course':bannar_course,
            'course_list':course_list,
            'org_list':org_list,
        })


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_wrong(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response