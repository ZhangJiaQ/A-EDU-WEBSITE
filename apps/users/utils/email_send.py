from random import Random

from django.core.mail import send_mail

from CourseEngine.settings import EMAIL_FORM
from apps.users.models import EmailVerifyRecord

def random_str(random_length=8):
    #生成长度为固定值的随机字符串
    string = ''
    chars = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        string += chars[random.randint(0,length)]

    return string

def send_register_email(email, send_type='register'):
    #先将生成好的字符串保存到数据库当中，
    email_record = EmailVerifyRecord()
    #调用生成随机字符串函数
    if send_type == 'update':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    #发送注册邮件
    if send_type == 'register':
        email_title = '慕课网激活链接'
        email_context = '您的激活链接为http://127.0.0.1:8000/active/{0}'.format(code)
        #利用Django内置的发送邮件发放发送邮件
        send_status = send_mail(email_title, email_context, EMAIL_FORM, [email])
        #如果发送状态为True，则执行下面逻辑
        if send_status:
            pass
    elif send_type == 'forgetpwd':
        email_title = '慕课网忘记密码'
        email_context = '您的修改密码链接为http://127.0.0.1:8000/reset/{0}'.format(code)
        # 利用Django内置的发送邮件发放发送邮件
        send_status = send_mail(email_title, email_context, EMAIL_FORM, [email])
        # 如果发送状态为True，则执行下面逻辑
        if send_status:
            pass
    elif send_type == 'update':
        email_title = '慕课网忘记密码'
        email_context = '您的验证码为{0}'.format(code)
        # 利用Django内置的发送邮件发放发送邮件
        send_status = send_mail(email_title, email_context, EMAIL_FORM, [email])
        # 如果发送状态为True，则执行下面逻辑
        if send_status:
            pass