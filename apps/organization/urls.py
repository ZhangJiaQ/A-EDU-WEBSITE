from django.conf.urls import url
from apps.organization.views import OrgView, AddUserAskView, OrgHomepageView, OrgCourseView, OrgTeacherView, \
    OrgDescView, AddFavView, TeacherListView, TeacherDetailView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    url(r'^homepage/(?P<org_id>\d+)/', OrgHomepageView.as_view(), name='org_homepage'),
    url(r'^course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name='org_course'),
    url(r'^org_teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name='org_teacher'),
    url(r'^desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name='org_desc'),

    #收藏课程机构URL
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
    #教师列表页
    url(r'^teacher_list/$', TeacherListView.as_view(), name='teacher_list'),
    #教师详情页
    url(r'^teacher/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]
