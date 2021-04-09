# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-11-15 09:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(max_length=16, verbose_name='槽位')),
                ('pd_type', models.CharField(max_length=16, verbose_name='类型')),
                ('capacity', models.CharField(max_length=16, verbose_name='容量')),
                ('model', models.CharField(max_length=32, verbose_name='型号')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='变更内容')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, '上线'), (2, '下线')], default=1, verbose_name='状态')),
                ('hostname', models.CharField(max_length=32, verbose_name='主机名')),
                ('last_date', models.DateField(blank=True, null=True, verbose_name='最新采集资产时间')),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Server', verbose_name='服务器'),
        ),
        migrations.AddField(
            model_name='disk',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Server', verbose_name='主机'),
        ),
    ]
