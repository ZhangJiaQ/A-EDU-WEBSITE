from django.conf.urls import url

from apps.users.views import UserInfoView, ImageUploadView

urlpatterns = [
    #用户信息中心
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    #用户头像上传
    url(r'^upload/$', ImageUploadView.as_view(), name='image_upload'),
]
