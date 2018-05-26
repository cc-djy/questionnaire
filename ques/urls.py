from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('', views.mbti, name='mbti')
]