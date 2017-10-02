from django.conf.urls import url

from apps.users.views import UserInfoView, ImageUploadView, UpdatePwd, UpdateEmail, UserCourseView, UserFavCourseView, \
    UserFavOrgView, UserFavTeacherView, UserMessageView

urlpatterns = [
    #用户信息中心
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    #用户头像上传
    url(r'^upload/$', ImageUploadView.as_view(), name='image_upload'),
    #更新密码
    url(r'^update/pwd/$', UpdatePwd.as_view(), name='update_pwd'),
    # 更新邮箱
    url(r'^update/email/$', UpdateEmail.as_view(), name='update_email'),
    #用户课程
    url(r'^course/$', UserCourseView.as_view(), name='user_course'),
    #用户收藏的机构
    url(r'^fav/org$', UserFavOrgView.as_view(), name='user_fav_org'),
    #用户收藏的课程
    url(r'^fav/course$', UserFavCourseView.as_view(), name='user_fav_course'),
    #用户收藏的教师
    url(r'^fav/teacher$', UserFavTeacherView.as_view(), name='user_fav_teacher'),
    #用户消息
    url(r'^message$', UserMessageView.as_view(), name='user_message'),
]
