from django.conf.urls import url

from apps.course.views import CourseView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView, \
    VideoPlayView


urlpatterns = [
    #课程列表页
    url(r'^list/$', CourseView.as_view(), name='course_list'),
    #课程详细信息页面
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    #课程章节页面
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    #课程评论页面
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    #添加评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    #课程视频播放页面
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='course_video'),
]
