from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Exam(models.Model):
    exam_name = models.CharField('The Exam', max_length=25)
    date = models.DateField('Date Held')
    duration = models.DurationField('Time Duration')

    def num_valid_questions(self):
        return len([q for q in self.mcqquestion_set.all() if q.check_if_valid()])

    def __str__(self):
        return str(self.exam_name) + ' held on ' + str(self.date)


class McqQuestion(models.Model):
    exam = models.ForeignKey(Exam, models.CASCADE)
    media = models.ImageField('Any image needed', upload_to='mcq_images/', blank=True, null=True)
    question = models.CharField('The MCQ Question', max_length=500)

    def __str__(self):
        return 'MCQ' + str(self.id) + ' of ' + str(self.exam.exam_name)[:10] + '<' + str(self.question)[:40] + '>'

    def get_choices(self):
        return list(self.mcqoption_set.all())

    def check_if_valid(self):
        return len(self.mcqoption_set.filter(is_correct=True)) == 1

    def get_answer(self):
        return self.mcqoption_set.filter(is_correct=True)[0] if self.check_if_valid() else None


class ExamPaper(models.Model):
    student = models.ForeignKey(User, models.CASCADE)
    exam = models.ForeignKey(Exam, models.DO_NOTHING, null=True)
    mcq_marks = models.PositiveIntegerField('Total MCQ paper marks', null=True)
    has_submitted = models.BooleanField("Paper is submitted", default=False)
    remaining_time = models.DurationField('Remaining Time', null=True)

    def __str__(self):
        return 'Exam Paper ' + 'of ' + str(self.student) + ' for ' + str(self.exam.exam_name)

    def total_marks(self):
        return self.mcq_marks + self.essay_marks


class McqOption(models.Model):
    question = models.ForeignKey(McqQuestion, models.CASCADE, null=False)
    option = models.CharField("Option for Question", max_length=200, null=False)
    is_correct = models.BooleanField("Tick the correct answer", default=False)

    def clean(self):
        super(McqOption, self).clean()
        model = self.question
        if model.mcqoption_set.count() > 4:
            raise ValidationError("Can only create 5 mcq options for '%s'" % model.question)

    def __str__(self):
        return f'Option for MCQ{str(self.question.id)} of {str(self.question.exam.exam_name)[:10]}'

