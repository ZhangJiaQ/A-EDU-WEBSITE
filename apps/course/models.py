from datetime import datetime

from django.db import models

from apps.organization.models import CourseOrg, Teacher


# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True)
    name = models.CharField(max_length=50, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(max_length=10, choices=(('cj','初级'),('zj','中级'),('gj','高级')), verbose_name='课程难度')
    learn_times = models.IntegerField(default=0, verbose_name='课程时间(分钟)')
    students = models.IntegerField(default=0, verbose_name='学生数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='courses/%Y/%M', verbose_name='封面图片')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(default='a', max_length=20, verbose_name='课程类别')
    tag = models.CharField(default='', max_length=10, verbose_name='课程标签')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    need_know = models.CharField(default='a', max_length=200, verbose_name='课程类别')
    teacher_tell = models.CharField(default='a', max_length=200, verbose_name='课程类别')
    teacher = models.ForeignKey(Teacher, verbose_name='教师', null=True, blank=True)


    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    def get_student_all(self):
        return self.usercourse_set.all()[:5]

    def get_lesson_all(self):
        return self.lesson_set.all()

    def get_resource_all(self):
        return self.courseresource_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_video_all(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    url = models.CharField(default='', max_length=100, verbose_name='url')
    learn_times = models.IntegerField(default=0, verbose_name='课程时间(分钟)')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='课程名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='下载路径')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name