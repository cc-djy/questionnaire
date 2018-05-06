from django.db import models

# Create your models here.

class TestPaper(models.Model):

    PaperID = models.AutoField(primary_key=True)

    PaperName = models.CharField(max_length=255)

    class Meta:

        db_table = "TestPaper"

        # 如果要将一个类的实例转化为str，则要定义__str__方法,相当于java中的toString



    def __str__(self):

        return ""





class Subject_Type(models.Model):

    Subject_TypeId = models.AutoField(primary_key=True)

    Description = models.CharField(max_length=255)

    PaperID = models.IntegerField()



    class Meta:

        db_table = "Subject_Type"



    # 如果要将一个类的实例转化为str，则要定义__str__方法,相当于java中的toString

    def __str__(self):

        return ""





class Question(models.Model):

    QuestionId = models.AutoField(primary_key=True)

    Question_Description = models.CharField(max_length=255)

    Subject_TypeId = models.IntegerField()



    class Meta:

        db_table = "Question"



    # 如果要将一个类的实例转化为str，则要定义__str__方法,相当于java中的toString

    def __str__(self):

        return ""





class Option(models.Model):

    OptionID = models.AutoField(primary_key=True)

    Option_Description = models.CharField(max_length=255)

    QuestionId = models.IntegerField()



    class Meta:

        db_table = "Option"



    # 如果要将一个类的实例转化为str，则要定义__str__方法,相当于java中的toString

    def __str__(self):

        return ""
