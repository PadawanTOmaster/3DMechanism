from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.generics import ListAPIView
import os
import json
from Myproject import settings
from rest_framework_jwt.settings import api_settings
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.views import obtain_jwt_token
from other_python import schoolnews
headers = {
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    "Access-Control-Allow-Origin": "*"
}


class SignupViewSet(APIView):
    def get(self, request):
        data = models1.userInfor.objects.all()
        serializer = SignupSerializer(data, many=True)
        return Response(serializer.data,headers=headers)
    
    def post(self,request):
        # 注册
        username = request.data['username']
        nickname = request.data['nickname']
        password = make_password(request.data['password'])
        email = request.data['email']
        information = request.data['information']
        avatar = request.FILES.get('avatar')

        if username in models1.userInfor.objects.values_list('username', flat=True):
            words = '这是一个已经存在的用户名，换一个吧'
            check = 0
            # 注册的用户名已存在
        else:
            # 新建
            if avatar is None:
                models1.userInfor.objects.create(
                    username=username,
                    nickname=nickname,
                    password=password,
                    email=email,
                    information=information,
                )
            else:
                models1.userInfor.objects.create(
                    username=username,
                    nickname=nickname,
                    password=password,
                    email=email,
                    information=information,
                    avatar=avatar,
                )
            words = '注册成功，请登录'
            check = 1
        data = {'alert': words, 'check': check}
        return Response(data, headers=headers)


class GetInforViewSet(APIView):
    def get(self,request,format=None):
        data = models1.userInfor.objects.all()
        serializer = GetInforSerializer(data, many=True)
        return Response(serializer.data,headers=headers)

    def post(self,request):
        username = request.data['username']
        userinfor = models1.userInfor.objects.get(username=username)
        data = {'nickname':userinfor.nickname ,'information':userinfor.information ,'avatar':str(userinfor.avatar)}
        return Response(data, headers=headers)


class DownloadFileViewSet(APIView):
    def get(self,request,format=None):
        data=models2.download.objects.all()
        serializer=DownloadFileSerializer(data,many=True)
        return Response(serializer.data,headers=headers)

    def post(self,request):
        filepath=request.FILES.get('filepath')
        imgpath = request.FILES.get('imgpath')
        filename = request.data['filename']
        description = request.data['description']
        models2.download.objects.create(
            filepath = filepath,
            imgpath = imgpath,
            filename = filename,
            description = description
        )
        data = {'alert:"提交成功"'}
        return Response(data,headers=headers)

    def delete(self,request):
        id = request.data['id']
        models2.download.objects.filter(id= id).delete()
        data={'alert':'删除成功'}
        return Response(data,headers=headers)

class EncyclopediaViewSet(APIView):
    def get(self,request,format=None):
        data=models4.encyclopedia.objects.all()
        serializer=EncyclopediaSerializer(data,many=True)
        return Response(serializer.data,headers=headers)


class FillblanksViewSet(APIView):
    def get(self,request):
        data=exercisemodel.fillblanks.objects.all()
        page = PageNumberPagination()
        # 每页显示条数
        page.page_size = 5
        page.page_query_param = 'page'
        page_list = page.paginate_queryset(data, request, view=self)
        serializer = FillblanksSerializer(instance=page_list,many=True)
        return page.get_paginated_response(serializer.data)


class DrawingViewSetPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'


class NewsViewSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class DrawingViewSet(ListAPIView):
    queryset = exercisemodel.drawing.objects.all()
    serializer_class = DrawingSerializer
    filter_fields = ('type',)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = DrawingViewSetPagination


class NewsViewSet(ListAPIView):
    queryset = newsmodel.schoolnews.objects.all().order_by('-release_time')
    serializer_class = NewsSerializer
    pagination_class = NewsViewSetPagination

    def post(self,request):
        if request.data['event']=='refresh':
            schoolnews.putintomysql()
            data={'alert':'刷新成功'}
            return Response(data,headers=headers)
