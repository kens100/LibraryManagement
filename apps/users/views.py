# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import UserProfile
from django.views.generic.base import View
from .forms import LoginForm
# from utils.email_send import send_forget_email


# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    def get(self, request):
        logout(request)

        return HttpResponse('{"status":"out"}', content_type='application/json')


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail"}', content_type='application/json')


class IndexView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        return render(request, "actionMenu.html")


# class ForgetPassWordView(View):
#     def get(self, request):
#         return render(request, 'resetPassword.html')
#
#     def post(self, request):
#         pwd = request.POST.get("password","")
#         pwd1 = request.POST.get("password1","")
#         email = request.POST.get("email","")
#         verify_code = request.POST.get("verifyCode","")
#         if pwd != pwd1:
#             return HttpResponse('{"status":0}', content_type='application/json')
#         verify_code_record = EmailVerifyRecord.objects.filter(email=email,code=verify_code)[0]
#         if verify_code_record:
#             dt = datetime.now()
#             if verify_code_record.end_time > dt:
#                 user = UserProfile.objects.get(email=email)
#                 user.password = make_password(pwd)
#                 user.save()
#                 return HttpResponse('{"status":1,"msg":"修改密码成功"}', content_type='application/json')
#             else:
#                 return HttpResponse('{"status":2,"msg":"验证码过期，修改密码失败"}', content_type='application/json')
#         else:
#             return HttpResponse('{"status":3,"msg":"验证码或邮箱不正确"}', content_type='application/json')
#
#
#
#
# class SendEmailCodeView(View):
#     def get(self, request):
#         email = request.GET.get('email', '')

        if not UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱未绑定用户"}', content_type='application/json')
        if send_forget_email(email)!=0:
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
