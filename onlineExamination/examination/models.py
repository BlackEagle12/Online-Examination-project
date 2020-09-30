from django.db import models

# Create your models here.

class Test(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateTimeField()
    close = models.DateTimeField()
    generated_by = models.CharField(max_length=100)
    description = models.TextField()
    instruction = models.TextField()
    total_marks = models.IntegerField()

class Question(models.Model):
    test_id = models.IntegerField()
    question = models.CharField(max_length=1000)
    mark = models.IntegerField()
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    correct_ans = models.CharField(max_length=100)

class Attempt(models.Model):
    user_id = models.CharField(max_length=100)
    test_id = models.IntegerField()
    submitted = models.BooleanField(default=False)

class Answer(models.Model):
    attempt_id = models.IntegerField()
    question_id = models.IntegerField()
    submitted_ans = models.CharField(max_length=100)
    obtained_marks = models.IntegerField()