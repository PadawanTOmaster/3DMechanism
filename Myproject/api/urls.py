from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views
urlpatterns = [
    path('signup/', views.SignupViewSet.as_view()),
    path('filedownload/', views.DownloadFileViewSet.as_view()),
    path('encyclopedia/', views.EncyclopediaViewSet.as_view()),
    path('fillblanks/', views.FillblanksViewSet.as_view()),
    path('drawing/',views.DrawingViewSet.as_view()),
    path('news/',views.NewsViewSet.as_view()),
    path('login/',obtain_jwt_token),
    path('getinfor/',views.GetInforViewSet.as_view()),
]
