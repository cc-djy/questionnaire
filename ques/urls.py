from django.urls import path

from ques import views

urlpatterns = [
    path('', views.hello, name='hello'),
]