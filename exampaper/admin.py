from django.contrib import admin
from .models import McqQuestions, Exam, EssayQuestion, ExamPaper, EssayAnswer, McqAnswer

admin.site.register(Exam)
admin.site.register(McqQuestions)
admin.site.register(EssayQuestion)
admin.site.register(ExamPaper)
admin.site.register(McqAnswer)
admin.site.register(EssayAnswer)
