from .models import Exam
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
            'duration': forms.TextInput(attrs={
                'type': 'hidden',
            }),
        }
