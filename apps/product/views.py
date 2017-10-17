# _*_ coding: utf-8 _*_
from django.shortcuts import render
import json
# Create your views here.
from django.core import serializers
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q
import simplejson

from .models import Product, Supplier
from operation.models import EnStore, OutStore
from users.models import UserProfile
from utils.email_send import send_warning_email


class GetWarningView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"done"}', content_type='application/json')
        products = Product.objects.all()
        for product in products:
            if product.min_count >= product.count:
                send_warning_email(request.user.email, product.name)
        return HttpResponse('{"status":"done"}', content_type='application/json')


class CheckView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        all_products = Product.objects.all()
        rows = []
        for product in all_products:
            if product.min_count >= product.count:
                rows.append(product)
        total = rows.__len__()

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "supplier":
                all_products = all_products.order_by("-supplier")
            elif sort == "name":
                all_products = all_products.order_by("-name")
            elif sort == "price":
                all_products = all_products.order_by("-price")
            elif sort == "add_time":
                all_products = all_products.order_by("-add_time")
        return render(request, "product_list.html", {
            "all_products": all_products,
            "sort": sort,
            "total": total,
        })

        # products = Product.objects.all()

        # return HttpResponse({"status": "nothing"}, content_type='application/json')


class EnStoreView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        return render(request, "enStore.html")

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        product = request.POST.get("product", "")
        supplier = request.POST.get("supplier", "")
        count = request.POST.get("count", 0)
        target_supplier = Supplier.objects.filter(name=supplier)
        if not target_supplier:
            return HttpResponse('{"status":"fail","msg":"入库失败，不存在该供应商"}', content_type='application/json')
        target_supplier = target_supplier[0]
        supplier_id = target_supplier.id
        oldProduct = Product.objects.filter(name=product, supplier=supplier_id)
        if not oldProduct:
            return HttpResponse('{"status":"fail","msg":"入库失败，请先添加该商品，再入库"}', content_type='application/json')
        oldProduct = oldProduct[0]
        if oldProduct.max_count is not None and oldProduct.max_count < (oldProduct.count + int(count)):
            return HttpResponse('{"status":"fail","msg":"入库失败，商品库存大于该商品允许的最大库存"}', content_type='application/json')
        oldProduct.count = oldProduct.count + int(count)
        oldProduct.save()
        enStoreRecord = EnStore()
        enStoreRecord.count = int(count)
        enStoreRecord.manager = request.user
        enStoreRecord.product = oldProduct
        enStoreRecord.supplier = target_supplier
        enStoreRecord.save()
        return HttpResponse('{"status":"success","msg":"入库成功"}', content_type='application/json')


class OutStoreView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        return render(request, "outStore.html")

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        product = request.POST.get("product", "")
        supplier = request.POST.get("supplier", "")
        count = request.POST.get("count", 0)
        target_supplier = Supplier.objects.filter(name=supplier)
        if not target_supplier:
            return HttpResponse('{"status":"fail","msg":"出库失败，不存在该供应商"}', content_type='application/json')
        target_supplier = target_supplier[0]
        supplier_id = target_supplier.id
        oldProduct = Product.objects.filter(name=product, supplier=supplier_id)
        if not oldProduct:
            return HttpResponse('{"status":"fail","msg":"出库失败，仓库没有该商品"}', content_type='application/json')
        oldProduct = oldProduct[0]
        if oldProduct.count < int(count):
            return HttpResponse('{"status":"fail","msg":"出库失败，商品库存小于你要的取货量"}', content_type='application/json')
        oldProduct.count = oldProduct.count - int(count)
        oldProduct.save()
        outStoreRecord = OutStore()
        outStoreRecord.count = int(count)
        outStoreRecord.manager = request.user
        outStoreRecord.product = oldProduct
        outStoreRecord.save()
        return HttpResponse('{"status":"success","msg":"出库成功"}', content_type='application/json')
