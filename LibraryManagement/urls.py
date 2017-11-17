"""LibraryManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.views.static import serve
from LibraryManagement.settings import STATIC_ROOT
import xadmin

from users.views import LoginView,IndexView,LogoutView,ForgetPassWordView,SendEmailCodeView
from book.views import OutStoreView,EnStoreView, OnBorrowView, OnReturnView, GetBookView
from press.views import AddPressView
from proof.views import AddProofView, GetProofView

urlpatterns = [
    url('^$', IndexView.as_view(), name='index'),
    url(r'^manage/', xadmin.site.urls, name='manage'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', LogoutView.as_view(), name='logout'),
    url('^forget/$', ForgetPassWordView.as_view(), name='forget'),
    url('^getEmail/$', SendEmailCodeView.as_view(), name='getEmail'),
    url('^outStore/$', OutStoreView.as_view(), name='outStore'),
    url('^enStore/$', EnStoreView.as_view(), name='enStore'),
    url('^onBorrow/$', OnBorrowView.as_view(), name='onBorrow'),
    url('^onReturn/$', OnReturnView.as_view(), name='onReturn'),
    url('^addPress/$', AddPressView.as_view(), name='addPress'),
    url('^addProof/$', AddProofView.as_view(), name='addProof'),
    url(r'^book/', include('book.urls', namespace="book")),
    url(r'^proof/', include('proof.urls', namespace="proof")),
    url(r'^getBook/$', GetBookView.as_view(), name="getBook"),
    url(r'^getProof/$', GetProofView.as_view(), name="getProof"),
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
