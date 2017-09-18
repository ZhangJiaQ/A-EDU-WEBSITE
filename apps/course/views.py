from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.course.models import Course, CourseResource
from apps.operation.models import UserFavorite, CourseComment, UserCourse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        #热门课程展示
        hot_courses = Course.objects.order_by('-click_nums')[:3]
        #课程排序规则
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


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        #增加课程点击数
        course.click_nums += 1
        course.save()

        #判断是否已经进行收藏
        has_fav_org = False
        has_fav_course = False
        if request.user.is_authenticated():
           if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
               has_fav_course = True
           if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=3):
               has_fav_org = True

        #相似课程推荐
        tag = course.tag
        if tag:
            likely_courses = Course.objects.filter(tag=tag)[:1]
        else:
            likely_courses = [] #防止html内for循环出错

        return render(request, 'course-detail.html', {
            'course':course,
            'likely_courses':likely_courses,
            'has_fav_org':has_fav_org,
            'has_fav_course':has_fav_course,
        })


class CourseInfoView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        #取出开始学习这门课程的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        #取出开始学习这门课程的所有用户的ID
        user_ids = [user_course.user.id for user_course in user_courses]
        #取出这些用户学习的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程的ID
        course_ids = [user_course.course.id for user_course in all_user_courses]
        #取出相关课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        return render(request, 'course-video.html', {
            'course': course,
            'relate_courses':relate_courses,
        })


class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course_comment = CourseComment.objects.filter(course=int(course_id))
        # 取出开始学习这门课程的所有用户
        user_courses = UserCourse.objects.filter(course=course)
        # 取出开始学习这门课程的所有用户的ID
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出这些用户学习的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的ID
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 取出相关课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        return render(request, 'course-comment.html', {
            'course': course,
            'course_comment': course_comment,
            'relate_courses': relate_courses,
        })


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            # 如果用户未登录，则返回登录页面
            return HttpResponse('{"status":"fail", "msg":"用户未登陆"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if course_id > 0 and course_id:
            course_comment = CourseComment()
            course_comment.user = request.user
            course_comment.course_comment = comments
            course_comment.course = Course.objects.get(id=int(course_id))
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')



