from django.db import models

# Create your models here.

class Ques(models.Model):
    title = models.CharField(max_length=100)  # 标题,限定长度最多一百
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)

    # 如果要将一个类的实例转化为str，则要定义__str__方法,相当于java中的toString
    def __str__(self):
        return self.title