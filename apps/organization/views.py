from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from .models import CourseOrg, CityDict
from .forms import UserAskForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from apps.operation.models import UserFavorite


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()

        #城市过滤筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #机构过滤筛选
        org_filter = request.GET.get('ct', '')
        if org_filter:
            all_orgs = all_orgs.filter(category=org_filter)

        #学生与课程人数排序
        nums_order = request.GET.get('sort', '')
        if nums_order == 'students':
            all_orgs = all_orgs.order_by('-student_nums')
        elif nums_order == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        #计算符合筛选课程数量
        org_num = CourseOrg.objects.count()

        #分页功能实现
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        #返回页面至前端
        return render(request, 'org-list.html', {
            'org_num':org_num,
            'all_citys':all_citys,
            'all_orgs':orgs,
            'city_id':city_id,
            'org_filter':org_filter
        })


class AddUserAskView(View):
    #配置用户咨询表单提交
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", msg:"添加出错"}')


class OrgHomepageView(View):

    def get(self, request, org_id):
        current_page = 'Homepage'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html', {
            'all_course':all_course,
            'all_teacher':all_teacher,
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgCourseView(View):

    def get(self, request, org_id):
        current_page = 'Course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_course = course_org.course_set.all()

        return render(request, 'org-detail-course.html', {
            'all_course':all_course,
            'course_org':course_org,
            'current_page': current_page,
        })


class OrgTeacherView(View):

    def get(self, request, org_id):
        current_page = 'Teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()

        return render(request, 'org-detail-teachers.html', {
            'all_teacher':all_teacher,
            'course_org': course_org,
            'current_page':current_page,
        })


class OrgDescView(View):

    def get(self, request, org_id):
        current_page = 'Desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        return render(request, 'org-detail-desc.html', {
            'course_org':course_org,
            'current_page': current_page,
        })


class AddFavView(View):

    def post(self, request):
        fav_id = request.POST.get('fav_id', '0')
        fav_type = request.POST.get('fav_type', '0')

        if not request.user.is_authenticated():
            #如果用户未登录，则返回登录页面
            return HttpResponse('{"status":"fail", "msg":"用户未登陆"}', content_type='application/json')

        exist_record =  UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            #如果收藏存在，则取消收藏
            exist_record.delete()
            return HttpResponse('{"status":"fail", "msg":"收藏"}', content_type='application/json')
        else:
            #如果收藏不存在，则收藏
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                #判断收藏是否合法
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"fail", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

