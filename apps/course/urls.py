from django.conf.urls import url

from apps.course.views import CourseView, CourseDetail

urlpatterns = [
    url(r'^list/$', CourseView.as_view(), name='org_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetail.as_view(), name='org_detail'),

]