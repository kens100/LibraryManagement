# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from press.models import Press
# Create your views here.
class AddPressView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        return render(request, "addPress.html")

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        name = request.POST.get("press", "")
        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")
        contact = request.POST.get("contact", "")
        if not name:
            return HttpResponse('{"status":"fail","msg":"添加失败，请输入出版社名称"}', content_type='application/json')
        target_press = Press.objects.filter(name=name)
        if target_press:
            return HttpResponse('{"status":"fail","msg":"添加失败，已存在该出版社"}', content_type='application/json')
        if not address:
            return HttpResponse('{"status":"fail","msg":"添加失败，请输入出版社地址"}', content_type='application/json')
        if not contact:
            return HttpResponse('{"status":"fail","msg":"添加失败，请输入联系人"}', content_type='application/json')
        press = Press()
        press.name = name
        press.phone = phone
        press.address = address
        press.contact = contact
        press.save()
        return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')