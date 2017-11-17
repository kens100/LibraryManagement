# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import ProofBorrowView, ProofListView


urlpatterns = [

    url(r'borrow', ProofBorrowView.as_view(), name="borrow_list"),
    url(r'list', ProofListView.as_view(), name="proof_list"),
]