from django.db import models

# Create your models here.

class TestPaper(models.Model):
    '''调查问卷'''
    paper_id = models.AutoField(primary_key=True)
    paper_name = models.CharField(max_length=512)

    class Meta:
        db_table = "test_paper"

    def __str__(self):
        return self.paper_id


class QuestionType(models.Model):
    '''题目类型以及描述'''
    question_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=512)
    paper_id = models.IntegerField()

    class Meta:
        db_table = "question_type"

    def __str__(self):
        return self.question_type_id

class Question(models.Model):
    '''问卷题目'''
    question_id = models.AutoField(primary_key=True)
    question_description = models.CharField(max_length=512)
    question_type_id = models.IntegerField()

    class Meta:
        db_table = "question"

    def __str__(self):
        return self.question_id


class Option(models.Model):
    '''问卷选项'''
    option_id = models.AutoField(primary_key=True)
    option_description = models.CharField(max_length=512)
    question_id = models.IntegerField()

    class Meta:
        db_table = "option"

    def __str__(self):
        return self.option_id
