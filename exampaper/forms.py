from .models import Exam, McqQuestion, McqOption
from django import forms


class ExamUpdateForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            'exam_name',
            'date',
            'duration',
        ]
        widgets = {
            'exam_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD'
            }),
            'duration': forms.HiddenInput(),
        }


class QuestionAddForm(forms.ModelForm):
    class Meta:
        model = McqQuestion
        fields = [
            'exam',
            'question',
            'media',
        ]
        widgets = {
            'question': forms.Textarea(attrs={
                'class': 'form-control',
                'cols': '40',
                'rows': '4',
                'maxlength': 500,
            }),
        }
