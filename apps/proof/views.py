# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from proof.models import Proof
# Create your views here.
class AddProofView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        return render(request, "addProof.html")

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        name = request.POST.get("proof", "")
        address = request.POST.get("address", "")
        id_number = request.POST.get("id_number", "")
        phone = request.POST.get("phone", "")
        if not id_number:
            return HttpResponse('{"status":"fail","msg":"添加失败，请输入ID号码"}', content_type='application/json')
        target_proof = Proof.objects.filter(id_number=id_number)
        if target_proof:
            return HttpResponse('{"status":"fail","msg":"添加失败，已存在该ID号码"}', content_type='application/json')
        if not name:
            return HttpResponse('{"status":"fail","msg":"添加失败，请输入借阅者名称"}', content_type='application/json')
        if not address:
            return HttpResponse('{"status":"fail","msg":"添加失败，请输入客户地址"}', content_type='application/json')
        if not phone:
            return HttpResponse('{"status":"fail","msg":"添加失败，请输入联系电话"}', content_type='application/json')
        proof = Proof()
        proof .name = name
        proof.address = address
        proof.id_number = id_number
        proof .phone = phone
        proof .save()
        return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')