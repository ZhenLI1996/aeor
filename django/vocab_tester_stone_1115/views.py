from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from vocab_tester.models import VocabTestQuestion, VocabTestRecord, Word
from model_manager.models import UserData

import random

# Create your views here.

from fractions import gcd
#TOTAL_QUESTION_CNT = VocabTestQuestion.objects.count()
#TOTAL_QUESTION_CNT = 10
#DIVIDE_PRIME = 13
#if gcd(TOTAL_QUESTION_CNT, DIVIDE_PRIME) > 1:
  #TOTAL_QUESTION_CNT -= 1

class Q():
  def __init__(self, question, A, B, C, D, correct, id):
    self.E = "没有正确答案"
    self.question = question
    self.A = A 
    self.B = B 
    self.C = C 
    self.D = D
    self.correct = correct
    self.id = id

def gen_rand_q(diff, q_answered_list):
  DIVIDE_PRIME = 13
  if diff > 3:
    diff = 3
  if diff < 1:
    diff = 1
  ret = Word.objects.filter(difficulty=diff)
  cnt = ret.count()
  if gcd(cnt, DIVIDE_PRIME) > 1:
    cnt -= 1
  r = int(random.randrange(0, cnt))
  w = ret[r]
  while w.id in q_answered_list:
    r = (r + DIVIDE_PRIME) % cnt
    w = ret[r]
  
  # 提取同样类别的词
  ret = Word.objects.filter(pos=w.pos)
  temp_l = len(ret)
  exp_list = []
  while len(exp_list) < 4:
    temp_w = ret[random.randrange(temp_l)]
    temp_e = temp_w.exp
    while temp_e in exp_list or temp_e == w.exp:
      temp_w = ret[random.randrange(temp_l)]
      temp_e = temp_w.exp
    exp_list.append(temp_w.pos + ' ' + temp_e)
  # 分配
  correct = chr(random.randrange(5) + 65)
  if correct == "A":
    return Q(question=w.word, A=w.pos+' '+w.exp, B=exp_list[1], C=exp_list[2], D=exp_list[3], correct=correct, id=w.id)
  elif correct == "B":
    return Q(question=w.word, A=exp_list[0], B=w.pos+' '+w.exp, C=exp_list[2], D=exp_list[3], correct=correct, id=w.id)
  elif correct == "C":
    return Q(question=w.word, A=exp_list[0], B=exp_list[1], C=w.pos+' '+w.exp, D=exp_list[3], correct=correct, id=w.id)
  elif correct == "D":
    return Q(question=w.word, A=exp_list[0], B=exp_list[1], C=exp_list[2], D=w.pos+' '+w.exp, correct=correct, id=w.id)
  else :
    return Q(question=w.word, A=exp_list[0], B=exp_list[1], C=exp_list[2], D=exp_list[3], correct=correct, id=w.id)
  
  '''
  ret = VocabTestQuestion.objects.filter(difficulty=diff)
  cnt = ret.count()
  if gcd(cnt, DIVIDE_PRIME) > 1:
    cnt -= 1
  r = int(random.randrange(0, cnt))
  q = ret[r]
  while q.id in q_answered_list:
    r = (r + DIVIDE_PRIME) % cnt
    q = ret[r]
  '''
  
  
@ensure_csrf_cookie
def index(request, param1=-1):
  if request.method == "POST" and 'q_id' in request.POST:
    # from previous question
    q_id = request.POST['q_id']
    q_answered_str = request.POST['q_answered']
    q_answered_list = q_answered_str.split(',')
    total_cnt = int(request.POST['total_cnt']) + 1
    correct_cnt = int(request.POST['correct_cnt'])
    cur_diff = int(request.POST['cur_diff'])
    '''
    if is_answer_correct(request.POST, q_id):
      correct_cnt += 1
    if total_cnt >= 10:    # all q answered
      return gen_result_page(request, total_cnt, correct_cnt, param1)
    else:
      return gen_next_q_page(request, q_id, total_cnt, correct_cnt, q_answered_list, param1)
    '''
    ans_rec_list = [int(i) for i in request.POST['ans_rec'].split(',')]
    ans_rec_list[(cur_diff-1)*2] += 1
    if is_answer_correct(request.POST, q_id):
      correct_cnt += 1
      ans_rec_list[(cur_diff-1)*2+1] += 1
    
    ans_rec = ','.join([str(i) for i in ans_rec_list])    
    if total_cnt >= 20:   # all answered
      return gen_result_page(request, total_cnt, correct_cnt, param1, ans_rec_list)
    elif total_cnt % 5 == 0:
      # change difficulty
      correct_ratio = ans_rec_list[(cur_diff-1)*2+1] / ans_rec_list[(cur_diff-1)*2]
      if correct_ratio > 0.6 and cur_diff < 3: 
        return gen_next_q_page(request, q_id, total_cnt, correct_cnt, q_answered_list, param1, cur_diff+1, ans_rec)
      elif correct_ratio <= 0.2 and cur_diff > 1:
        return gen_next_q_page(request, q_id, total_cnt, correct_cnt, q_answered_list, param1, cur_diff-1, ans_rec)
      else:
        return gen_next_q_page(request, q_id, total_cnt, correct_cnt, q_answered_list, param1, cur_diff, ans_rec)
    else:
      # do not change difficulty 
        return gen_next_q_page(request, q_id, total_cnt, correct_cnt, q_answered_list, param1, cur_diff, ans_rec)
    
    
  else:
    # new start 
    return gen_first_q_page(request, param1) 

    

@ensure_csrf_cookie
def gen_first_q_page(request, user_id):
  data = {}
  #target_id = random.randrange(1, TOTAL_QUESTION_CNT)
  #q = VocabTestQuestion.objects.get(id=target_id)
  q = gen_rand_q(1, [])
  data['total_cnt'] = 0
  data['correct_cnt'] = 0
  data['question'] = q.question
  data['A'] = q.A
  data['B'] = q.B
  data['C'] = q.C
  data['D'] = q.D
  data['E'] = q.E
  data['q_id'] = q.id
  data['correct'] = q.correct
  data['q_answered'] = ''
  data['user_id'] = user_id
  data['ans_rec'] = ','.join(['0','0']*11)
  data['cur_diff'] = '1'
  return render(request, "vocab_test/index.html", data)

    
@ensure_csrf_cookie
def gen_next_q_page(request, last_id, total_cnt, correct_cnt, q_answered_list, user_id, diff, ans_rec):
  data = {}
  #target_id = gen_rand_q(diff, q_answered_list)
  q = gen_rand_q(diff, q_answered_list)
  q_answered_list.append(str(q.id))
  data['total_cnt'] = total_cnt
  data['correct_cnt'] = correct_cnt
  data['question'] = q.question
  data['A'] = q.A
  data['B'] = q.B
  data['C'] = q.C
  data['D'] = q.D
  data['E'] = q.E
  data['q_id'] = q.id
  data['correct'] = q.correct
  data['q_answered'] = ','.join(q_answered_list)
  data['user_id'] = user_id
  data['ans_rec'] = ans_rec
  data['cur_diff'] = diff
  return render(request, "vocab_test/index.html", data)
  
def is_answer_correct(POST, target_id):
  #answer = POST['correct_answer']
  #q = Word.objects.get(id=target_id)
  if POST['answer'] == POST['correct']:
    return True
  else:
    return False
  

def gen_result_page(request, total_cnt, correct_cnt, user_id, ans_rec_list):
  data = {}
  data['total_cnt'] = total_cnt
  data['correct_cnt'] = correct_cnt
  data['user_name'] = ''

  details = ['lvl:{}, total:{}, correct:{}'.format(i+1, ans_rec_list[2*i], ans_rec_list[2*i+1]) for i in range(3)]
  data['details'] = '\n<br />\n'.join(details) 

  if int(user_id) > 0: 
    user = UserData.objects.get(id=user_id)
    data['user_name'] = user._name
    record = VocabTestRecord(user_id=user_id, user_name=user._name, total_cnt=total_cnt, correct_cnt=correct_cnt)
    record.save()
    
  return render(request, "vocab_test/result.html", data)

  
  
def blackhole(request):
  if request.method == "POST" and 'answer' in request.POST and 'q_id' in request.POST:
    answer = request.POST['answer']
    q_id = request.POST['q_id']
  else:
    answer = 'default'
    q_id = 1
  q = VocabTestQuestion.objects.get(id=q_id)
  correct = q.correct
  data = {}
  data['answer'] = answer
  data['last_q_id'] = q_id
  
  if correct == answer:
    data['result'] = 'cong!'
  else:
    data['result'] = 'cheer up!'
  
  return render(request, "vocab_test/blackhole.html", data)
  
