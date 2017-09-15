from django.shortcuts import render
from django.views import View

from apps.course.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.order_by('-click_nums')[:3]

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')
        elif sort == 'student':
            all_courses = all_courses.order_by('-students')

        # 分页功能实现
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 9, request=request)

        courses = p.page(page)

        #返回页面至前端
        return render(request, 'course-list.html', {
            'all_courses':courses,
            'sort':sort,
            'hot_courses':hot_courses,
        })

class CourseDetail(View):
    def get(self, request, course_id):
        return render(request, 'course-detail.html', {
        })