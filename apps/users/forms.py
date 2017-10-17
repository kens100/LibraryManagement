# -*- coding: utf-8 -*-
# __author__ = 'qingqinglei'
# __date__ = '2017/6/13 10:10'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)