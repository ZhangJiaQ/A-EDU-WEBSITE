"""CourseEngine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.static import serve

import xadmin
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from CourseEngine.settings import MEDIA_ROOT, STATIC_ROOT
from apps.users.views import LoginView, RegisterView, ActiveUser, ForgetPsd, ResetPwd, ModefyPwd, IndexView, LogoutView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #用户操作
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUser.as_view(), name='active_user'),
    url(r'^forget/$', ForgetPsd.as_view(), name='forgetpwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetPwd.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModefyPwd.as_view(), name='modify_pwd'),
    #分发URL至机构列表
    url(r'^org/', include('apps.organization.urls', namespace='org')),
    #返回图片至前端
    url(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),
    #返回图片至前端
    url(r'^static/(?P<path>.*)$', serve, {'document_root':STATIC_ROOT}),
    #分发URL至课程列表
    url(r'^course/', include('apps.course.urls', namespace='course')),
    # 分发URL至用户列表
    url(r'^users/', include('apps.users.urls', namespace='users')),
]


handler404 = 'apps.users.views.page_not_found'

handler500 = 'apps.users.views.page_wrong'