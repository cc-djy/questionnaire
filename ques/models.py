from django.db import models

# Create your models here.

class TestPaper(models.Model):
    '''调查问卷'''
    paper_id = models.AutoField(primary_key=True)
    paper_name = models.CharField(max_length=255)

    class Meta:
        db_table = "test_paper"

    # 如果要将一个类的实例转化为str，则要定义__str__方法,相当于java中的toString
    def __str__(self):
        return ""


class SubjectType(models.Model):
    '''问卷类型以及描述'''
    subject_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    paper_id = models.IntegerField()

    class Meta:
        db_table = "subject_type"

    def __str__(self):
        return ""

class Question(models.Model):
    '''问卷题目'''
    question_id = models.AutoField(primary_key=True)
    question_description = models.CharField(max_length=255)
    subject_type_id = models.IntegerField()

    class Meta:
        db_table = "question"

    def __str__(self):
        return ""


class Option(models.Model):
    '''问卷选项'''
    option_id = models.AutoField(primary_key=True)
    option_description = models.CharField(max_length=255)
    question_id = models.IntegerField()

    class Meta:
        db_table = "option"

    def __str__(self):
        return ""
