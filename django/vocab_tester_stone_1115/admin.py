from django.contrib import admin
from vocab_tester.models import VocabTestQuestion, VocabTestRecord

# Register your models here.

def show_difficulty(obj):
  if obj.difficulty == -1:
    return '未知难度'
  else:
    return str(obj.difficulty)

class VocabTestQuestionAdmin(admin.ModelAdmin):
  list_display = ('id', 'question', 'A', 'B', 'C', 'D', 'E', 'correct', show_difficulty) # list
  fields = ('question', 'A', 'B', 'C', 'D', 'E', 'correct', 'difficulty')
  #def has_add_permission(self, request):
    #return False
admin.site.register(VocabTestQuestion, VocabTestQuestionAdmin)



class VocabTestRecordAdmin(admin.ModelAdmin):
  list_display = ('id', 'user_id', 'user_name', 'total_cnt', 'correct_cnt') # list
  def has_add_permission(self, request):
    return False
admin.site.register(VocabTestRecord, VocabTestRecordAdmin)