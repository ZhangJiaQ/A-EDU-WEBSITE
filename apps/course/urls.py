from django.conf.urls import url

from apps.course.views import CourseView

urlpatterns = [
    url(r'^list/$', CourseView.as_view(), name='org_list'),

]