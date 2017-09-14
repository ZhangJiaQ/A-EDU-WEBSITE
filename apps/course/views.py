from django.shortcuts import render
from django.views import View

from apps.course.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all()

        # 分页功能实现
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 9, request=request)

        courses = p.page(page)

        #返回页面至前端
        return render(request, 'course-list.html', {
            'all_courses':courses
        })