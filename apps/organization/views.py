from django.shortcuts import render

# Create your views here.
from django.views import View

from .models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


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
            'org_filter':org_filter,
        })
