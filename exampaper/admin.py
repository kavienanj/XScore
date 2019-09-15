from django.contrib import admin
from .models import McqQuestion, Exam, EssayQuestion, EssayAnswer, McqOption, ExamPaper

admin.site.register(Exam)
admin.site.register(McqQuestion)
admin.site.register(EssayQuestion)
admin.site.register(ExamPaper)
admin.site.register(McqOption)
admin.site.register(EssayAnswer)
