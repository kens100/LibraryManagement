# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-18 00:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
        ('proof', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book', verbose_name='\u4e66\u7c4d')),
                ('proof', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proof.Proof', verbose_name='\u501f\u9605\u8005')),
            ],
            options={
                'verbose_name': '\u5165\u5e93\u8bb0\u5f55',
                'verbose_name_plural': '\u5165\u5e93\u8bb0\u5f55',
            },
        ),
    ]
