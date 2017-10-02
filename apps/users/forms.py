from django import forms

from apps.users.models import UserProfile
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class ImageUploadForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['nickname', 'birday', 'gender', 'address', 'mobile']

