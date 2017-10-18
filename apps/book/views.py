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

from .models import Book, Press
from operation.models import EnStore, OutStore
from users.models import UserProfile
from utils.email_send import send_warning_email


class GetWarningView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"done"}', content_type='application/json')
        books = Book.objects.all()
        for book in books:
            if book.min_count >= book.count:
                send_warning_email(request.user.email, book.name)
        return HttpResponse('{"status":"done"}', content_type='application/json')


class CheckView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        all_books = Book.objects.all()
        rows = []
        for product in all_books:
            if product.min_count >= product.count:
                rows.append(product)
        total = rows.__len__()

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "supplier":
                all_books = all_books.order_by("-supplier")
            elif sort == "name":
                all_books = all_books.order_by("-name")
            elif sort == "price":
                all_books = all_books.order_by("-price")
            elif sort == "add_time":
                all_books = all_books.order_by("-add_time")
        return render(request, "product_list.html", {
            "all_products": all_books,
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
        target_press = Press.objects.filter(name=supplier)
        if not target_press:
            return HttpResponse('{"status":"fail","msg":"入库失败，不存在该出版社"}', content_type='application/json')
        target_press = target_press[0]
        supplier_id = target_press.id
        oldBook = Book.objects.filter(name=product, supplier=supplier_id)
        if not oldBook:
            return HttpResponse('{"status":"fail","msg":"入库失败，请先添加该书籍，再入库"}', content_type='application/json')
        # oldBook = oldBook[0]
        # if oldBook.max_count is not None and oldBook.max_count < (oldBook.count + int(count)):
        #     return HttpResponse('{"status":"fail","msg":"入库失败，书籍库存大于该书籍允许的最大库存"}', content_type='application/json')
        oldBook.max_amount = oldBook.max_amount + int(count)
        oldBook.save()
        enStoreRecord = EnStore()
        enStoreRecord.count = int(count)
        enStoreRecord.manager = request.user
        enStoreRecord.book = oldBook
        enStoreRecord.supplier = target_press
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
        target_press = Press.objects.filter(name=supplier)
        if not target_press:
            return HttpResponse('{"status":"fail","msg":"出库失败，不存在该出版社"}', content_type='application/json')
        target_press = target_press[0]
        supplier_id = target_press.id
        oldBook = Book.objects.filter(name=product, supplier=supplier_id)
        if not oldBook:
            return HttpResponse('{"status":"fail","msg":"出库失败，仓库没有该书籍"}', content_type='application/json')
        oldBook = oldBook[0]
        if (oldBook.max_amcount - oldBook.borrow_amount) < int(count):
            return HttpResponse('{"status":"fail","msg":"出库失败，书籍库存小于你要的取货量"}', content_type='application/json')
        oldBook.max_amcount = oldBook.max_amcount - int(count)
        oldBook.save()
        outStoreRecord = OutStore()
        outStoreRecord.count = int(count)
        outStoreRecord.manager = request.user
        outStoreRecord.book = oldBook
        outStoreRecord.save()
        return HttpResponse('{"status":"success","msg":"出库成功"}', content_type='application/json')
