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
from datetime import datetime

from .models import Book, Press
from operation.models import EnStore, OutStore
from users.models import UserProfile
from borrow.models import Borrow
from proof.models import Proof


class GetWarningView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"done"}', content_type='application/json')
        books = Book.objects.all()
        for book in books:
            if book.min_count >= book.count:
                pass
                # send_warning_email(request.user.email, book.name)
        return HttpResponse('{"status":"done"}', content_type='application/json')


class BookListView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        all_books = Book.objects.all()
        rows = []
        for book in all_books:
            rows.append(book)
        total = rows.__len__()

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "name":
                all_books = all_books.order_by("-name")
            elif sort == "writer":
                all_books = all_books.order_by("-writer")
            elif sort == "press":
                all_books = all_books.order_by("-press")
            elif sort == "price":
                all_books = all_books.order_by("-price")
            elif sort == "max_amount":
                all_books = all_books.order_by("-max_amount")
            elif sort == "add_time":
                all_books = all_books.order_by("-add_time")
        return render(request, "book_list.html", {
            "all_books": all_books,
            "sort": sort,
            "total": total,
        })

        # products = Product.objects.all()

        # return HttpResponse({"status": "nothing"}, content_type='application/json')



#出库
class OutStoreView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.has_perm('add_outstore'):
            return render(request, "403.html")
        return render(request, "outStore.html")

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.has_perm('add_outstore'):
            return render(request, "403.html")

        book = request.POST.get("book", "")
        press = request.POST.get("press", "")
        count = request.POST.get("count", 0)
        target_press = Press.objects.filter(name=press)
        if not target_press:
            return HttpResponse('{"status":"fail","msg":"出库失败，不存在该出版社"}', content_type='application/json')
        target_press = target_press[0]
        press_id = target_press.id
        oldBook = Book.objects.filter(name=book, press=press_id)
        if not oldBook:
            return HttpResponse('{"status":"fail","msg":"出库失败，仓库没有该书籍"}', content_type='application/json')
        oldBook = oldBook[0]
        if (oldBook.max_amount - oldBook.borrow_amount) < int(count):
            return HttpResponse('{"status":"fail","msg":"出库失败，书籍库存小于你要的取货量"}', content_type='application/json')
        oldBook.max_amount = oldBook.max_amount - int(count)
        oldBook.save()
        outStoreRecord = OutStore()
        outStoreRecord.count = int(count)
        outStoreRecord.manager = request.user
        outStoreRecord.book = oldBook
        outStoreRecord.save()
        return HttpResponse('{"status":"success","msg":"出库成功"}', content_type='application/json')

#入库
class EnStoreView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.has_perm('add_enstore'):
            return render(request, "403.html")
        return render(request, "enStore.html")

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.has_perm('add_enstore'):
            return render(request, "403.html")

        book = request.POST.get("book", "")
        press = request.POST.get("press", "")
        count = request.POST.get("count", 0)
        target_press = Press.objects.filter(name=press)
        if not target_press:
            return HttpResponse('{"status":"fail","msg":"入库失败，不存在该出版社"}', content_type='application/json')
        target_press = target_press[0]
        press_id = target_press.id
        oldBook = Book.objects.filter(name=book, press=press_id)
        if not oldBook:
            return HttpResponse('{"status":"fail","msg":"入库失败，请先添加该书籍，再入库"}', content_type='application/json')
        oldBook = oldBook[0]
        if int(count) <= 0:
            return HttpResponse('{"status":"fail","msg":"输入数字必须大于0"}', content_type='application/json')
        oldBook.max_amount = oldBook.max_amount + int(count)
        oldBook.save()
        enStoreRecord = EnStore()
        enStoreRecord.count = int(count)
        enStoreRecord.manager = request.user
        enStoreRecord.book = oldBook
        enStoreRecord.press = target_press
        enStoreRecord.save()
        return HttpResponse('{"status":"success","msg":"入库成功"}', content_type='application/json')

#借阅
class OnBorrowView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.has_perm('borrow.change_borrow'):
            return render(request, "403.html")
        return render(request, "onBorrow.html")

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.has_perm('borrow.change_borrow'):
            return render(request, "403.html")

        proof = request.POST.get("proof", "")
        book = request.POST.get("book", "")
        press = request.POST.get("press", "")
        target_proof = Proof.objects.filter(name=proof)
        if not target_proof:
            return HttpResponse('{"status":"fail","msg":"查询失败，不存在该借阅者"}', content_type='application/json')
        target_proof = target_proof[0]
        proof_id = target_proof.id
        target_press = Press.objects.filter(name=press)
        if not target_press:
            return HttpResponse('{"status":"fail","msg":"查询失败，不存在该出版社"}', content_type='application/json')
        target_press = target_press[0]
        press_id = target_press.id
        oldBook = Book.objects.filter(name=book, press=press_id)
        if not oldBook:
            return HttpResponse('{"status":"fail","msg":"查询失败，仓库没有该书籍"}', content_type='application/json')
        oldBook = oldBook[0]
        if (oldBook.max_amount - oldBook.borrow_amount) < 1:
            return HttpResponse('{"status":"fail","msg":"借阅失败，书籍库存小于你要的取货量"}', content_type='application/json')
        oldBook.borrow_amount = oldBook.borrow_amount + 1
        oldBook.save()
        onBorrowRecord = Borrow()
        onBorrowRecord.book = oldBook
        onBorrowRecord.proof = target_proof
        onBorrowRecord.save()
        return HttpResponse('{"status":"success","msg":"借阅成功"}', content_type='application/json')

#还书
class OnReturnView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.has_perm('borrow.change_borrow'):
            return render(request, "403.html")
        return render(request, "onReturn.html")

    def post(self, request):
        if not request.user.is_authenticated():
            return render(request, "login.html")
        if not request.user.has_perm('borrow.change_borrow'):
            return render(request, "403.html")

        proof = request.POST.get("proof", "")
        book = request.POST.get("book", "")
        press = request.POST.get("press", "")
        target_proof = Proof.objects.filter(name=proof)
        if not target_proof:
            return HttpResponse('{"status":"fail","msg":"查询失败，不存在该借阅者"}', content_type='application/json')
        target_proof = target_proof[0]
        proof_id = target_proof.id
        target_press = Press.objects.filter(name=press)
        if not target_press:
            return HttpResponse('{"status":"fail","msg":"查询失败，不存在该出版社"}', content_type='application/json')
        target_press = target_press[0]
        press_id = target_press.id
        oldBook = Book.objects.filter(name=book, press=press_id)
        if not oldBook:
            return HttpResponse('{"status":"fail","msg":"查询失败，仓库没有该书籍"}', content_type='application/json')
        oldBook = oldBook[0]
        book_id = oldBook.id
        borrow_record_list = Borrow.objects.filter(book=book_id, proof=proof_id)
        target_borrow = None
        if not borrow_record_list:
            return HttpResponse('{"status":"fail","msg":"查询失败，没有该借阅记录"}', content_type='application/json')
        for borrow_record in borrow_record_list:
            if not borrow_record.return_time:
                target_borrow = borrow_record
                break
        if not target_borrow:
            return HttpResponse('{"status":"fail","msg":"查询失败，没有该借阅记录"}', content_type='application/json')
        if oldBook.borrow_amount < 1:
            return HttpResponse('{"status":"fail","msg":"还书失败，书籍库存小于你要的取货量"}', content_type='application/json')
        target_borrow.return_time = datetime.now()
        target_borrow.save()
        oldBook.borrow_amount = oldBook.borrow_amount - 1
        oldBook.save()
        return HttpResponse('{"status":"success","msg":"还书成功"}', content_type='application/json')


class GetBookView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return
        if not request.user.has_perm('borrow.change_borrow'):
            return

        book_id = request.POST.get("book_id", "")
        target_book = Book.objects.filter(id=book_id)
        if not target_book:
            return

        target_book = target_book[0]
        target_press = target_book.press
        if not target_press:
            return

        book_info = {
            'book_name': target_book.name,
            'book_press': target_press.name,
        }
        return HttpResponse(json.dumps(book_info), content_type='application/json')