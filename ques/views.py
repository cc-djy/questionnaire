from django.shortcuts import render
from django.views.decorators.cache import cache_page
# from .models import Ques


# Create your views here.


@cache_page(60 * 15)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def index(request):
    # 读取题目
    context = {}
    # context['topics'] = Ques.objects.all()

    # 读取数据库等 并渲染到网页
    return render(request, 'index.html', context)

