from django.contrib import admin
from django.db import models

# Create your models here.



class TestPaper(models.Model):
    """
    调查问卷
    """
    paper_id = models.AutoField(primary_key=True)
    paper_name = models.CharField(max_length=512)

    class Meta:
        db_table = "test_paper"

    def __str__(self):
        return self.paper_id


class QuestionType(models.Model):
    """
    题目类型以及描述
    """
    question_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=512)
    paper_id = models.IntegerField()

    class Meta:
        db_table = "question_type"

    def __str__(self):
        return self.question_type_id


class Question(models.Model):
    """
    问卷题目
    """
    question_id = models.AutoField(primary_key=True)
    question_description = models.CharField(max_length=512)
    question_type_id = models.IntegerField()

    class Meta:
        db_table = "question"

    def __str__(self):
        return self.question_id


class Option(models.Model):
    """
    问卷选项
    """
    option_id = models.AutoField(primary_key=True)
    option_description = models.CharField(max_length=512)
    question_id = models.IntegerField()

    class Meta:
        db_table = "option"

    def __str__(self):
        return self.option_id


class CommitRecord(models.Model):
    """
    提交信息记录
    """
    commit_id = models.AutoField(primary_key=True)
    user_openid = models.CharField(max_length=256)
    user_id = models.CharField(max_length=32)
    client_time = models.DateTimeField()
    server_time = models.DateTimeField()

    class Meta:
        db_table = "commit_record"

    def __str__(self):
        return 'commit_record {}'.format(self.commit_id)


class SelectRecord(models.Model):
    """
    用户选题信息记录
    """
    commit_id = models.IntegerField()
    question_id = models.IntegerField()
    option_id = models.IntegerField()

    class Meta:
        db_table = "select_record"

    def __str__(self):
        return 'select_record {}'.format(self.commit_id)


class SelectRecordAdmin(admin.ModelAdmin):
    list_display = ("commit_id", "question_id", "option_id")

class CommitRecordAdmin(admin.ModelAdmin):
    list_display = ("commit_id", "user_openid", "user_id")