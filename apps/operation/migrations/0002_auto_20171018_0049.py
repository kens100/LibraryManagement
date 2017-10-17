# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-18 00:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('operation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='outstore',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u804c\u5de5'),
        ),
        migrations.AddField(
            model_name='outstore',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='\u5546\u54c1'),
        ),
        migrations.AddField(
            model_name='enstore',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u804c\u5de5'),
        ),
        migrations.AddField(
            model_name='enstore',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='\u5546\u54c1'),
        ),
        migrations.AddField(
            model_name='enstore',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.Supplier', verbose_name='\u4f9b\u5e94\u5546'),
        ),
    ]
