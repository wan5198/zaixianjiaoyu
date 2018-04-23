from django import forms
from captcha.fields import CaptchaField
#login验证
class LoginForm(forms.Form):
    username = forms.CharField(min_length=5,required=True)
    password =forms.CharField(min_length=6,required=True)

#注册表单验证
class RegForm(forms.Form):
    email = forms.EmailField()
    password =forms.CharField(min_length=6)
    captcha = CaptchaField()

#找回密码表单
class ForgetPwdFprm(forms.Form):
    email = forms.EmailField(required=True)
    captcha=CaptchaField(error_messages={'invaild':'请输入正确的验证码'})

#密码修改表单
class ModifyPwdForm(forms.Form):
    '''重置密码'''
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
    email = forms.EmailField()