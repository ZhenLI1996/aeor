from django.db import models
import random

# Create your models here.
class VocabTestQuestion(models.Model):
  #pass
  question = models.CharField(max_length=128, default='new word', verbose_name="问题")
  A = models.CharField(max_length=128, default='第一种意思', verbose_name="第一个选项")
  B = models.CharField(max_length=128, default='第二种意思', verbose_name="第二个选项")
  C = models.CharField(max_length=128, default='第三种意思', verbose_name="第三个选项")
  D = models.CharField(max_length=128, default='第四种意思', verbose_name="第四个选项")
  E = models.CharField(max_length=128, default='无正确答案', verbose_name="第五个选项")
  correct = models.CharField(max_length=16, default='A', verbose_name="正确答案")
  difficulty = models.IntegerField(default=-1, verbose_name="难度等级")
  ''' difficulty level:
    -1    : unknown
    1-10  : easy to hard
  '''
    
  class Meta:
    verbose_name = '词汇量测试题'
    verbose_name_plural = '词汇量测试题'
  

class VocabTestRecord(models.Model):
  user_id = models.IntegerField(verbose_name="用户ID")
  user_name = models.CharField(verbose_name="微信名", max_length=128)
  total_cnt = models.IntegerField(verbose_name="总答题数")
  correct_cnt = models.IntegerField(verbose_name="正确数")
  class Meta:
    verbose_name = '词汇量测试记录'
    verbose_name_plural = '词汇量测试记录'
    

class Word(models.Model):
  word = models.CharField(max_length=128, default='new word', verbose_name="词")
  pos = models.CharField(max_length=128, default='new word', verbose_name="词")
  exp = models.CharField(max_length=128, default='new word', verbose_name="词")
  difficulty = models.IntegerField(default=0, verbose_name="难度等级")
