from django.contrib import admin
from .models import McqQuestion, Exam, McqOption, ExamPaper

admin.site.register(Exam)
admin.site.register(McqQuestion)
admin.site.register(ExamPaper)
admin.site.register(McqOption)
