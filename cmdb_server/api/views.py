from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from django.db.models import Q
import datetime
from rest_framework.throttling import BaseThrottle

# Create your views here.


class ServerView(APIView):

    def get(self,request,*args,**kwargs):
        today = datetime.datetime.today()

        # 判断服务器的状态以及最后一次收集信息的时间，来确认需要收集数据的主机
        queryset = models.Server.objects.filter(status=1).filter(Q(last_date__isnull=True)|Q(last_date__lt=today)).values("hostname")

        # 组成列表
        host_list = [item['hostname'] for item in queryset]
        return Response(host_list)

    def post(self,request,*args,**kwargs):
        hostname = request.data.get('hostname')
        hostname_obj = models.Server.objects.filter(hostname=hostname).first()
        if not hostname:
            return Response('主机不存在')


        print(request.data)
        return Response('ok')
