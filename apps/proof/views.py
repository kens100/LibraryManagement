# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth.models import Group
import json

from proof.models import Proof
from borrow.models import Borrow
from users.models import UserProfile
# Create your views here.
class AddProofView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.has_perm('proof.add_proof'):
            return render(request, "403.html")
        return render(request, "addProof.html")

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        name = request.POST.get("proof", "")
        sex = request.POST.get("sex", "")
        address = request.POST.get("address", "")
        id_number = request.POST.get("id_number", "")
        phone = request.POST.get("phone", "")
        if not id_number:
            return HttpResponse('{"status":"fail","msg":"添加失败，请输入ID号码"}', content_type='application/json')
        target_proof = Proof.objects.filter(id=id_number)
        if target_proof:
            return HttpResponse('{"status":"fail","msg":"添加失败，已存在该ID号码"}', content_type='application/json')
        if not name:
            return HttpResponse('{"status":"fail","msg":"添加失败，请输入借阅者名称"}', content_type='application/json')
        if int(sex) < 1 or int(sex) > 2:
            return HttpResponse('{"status":"fail","msg":"添加失败，性别选项错误"}', content_type='application/json')
        if not address:
            return HttpResponse('{"status":"fail","msg":"添加失败，请输入客户地址"}', content_type='application/json')
        if not phone:
            return HttpResponse('{"status":"fail","msg":"添加失败，请输入联系电话"}', content_type='application/json')
        proof = Proof()
        proof.id = id_number
        proof.name = name
        proof.sex = sex
        proof.address = address
        proof .phone = phone
        proof .save()
        new_user = UserProfile.objects.create_user(username=proof.id, password='l' + str(proof.id))
        new_user.is_staff = True
        new_user.groups.add(Group.objects.get(name='Visitor'))
        new_user.save()
        return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')


class ProofBorrowView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.has_perm('borrow.admin_borrow'):
            proof_id = request.user.username
        else:
            proof_id = request.GET.get('id', "")
        proof = Proof.objects.filter(id=proof_id)
        if not proof:
            return render(request, "proof_borrow_list.html", {
                "proof_borrows": None,
                "total": 0,
            })
        proof = proof[0]
        proof_borrows = Borrow.objects.filter(proof=proof)
        rows = []
        for borrow in proof_borrows:
            rows.append(borrow)
        total = rows.__len__()

        proof_borrows = proof_borrows.order_by("return_time")
        return render(request, "proof_borrow_list.html", {
            "proof": proof,
            "proof_borrows": proof_borrows,
            "total": total,
        })

class GetProofView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return
        if not request.user.has_perm('borrow.change_borrow'):
            return

        proof_id = request.POST.get("proof_id", "")
        target_proof = Proof.objects.filter(id=proof_id)
        if target_proof:
            target_proof = target_proof[0]
            proof_info = {'proof_name': target_proof.name,}
            return HttpResponse(json.dumps(proof_info), content_type='application/json')

class ProofListView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        all_proofs = Proof.objects.all()
        rows = []
        for proof in all_proofs:
            rows.append(proof)
        total = rows.__len__()

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "name":
                all_proofs = all_proofs.order_by("-name")
            elif sort == "sex":
                all_proofs = all_proofs.order_by("-sex")
            elif sort == "address":
                all_proofs = all_proofs.order_by("-address")
            elif sort == "phone":
                all_proofs = all_proofs.order_by("-phone")
            elif sort == "now_borrow_amount":
                all_proofs = all_proofs.order_by("-now_borrow_amount")
            elif sort == "add_time":
                all_proofs = all_proofs.order_by("-add_time")
        return render(request, "proof_list.html", {
            "all_proofs": all_proofs,
            "sort": sort,
            "total": total,
        })