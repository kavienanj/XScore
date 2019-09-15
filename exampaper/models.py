from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Exam(models.Model):
    exam_name = models.CharField('The Exam', max_length=25)
    date = models.DateField('Date Held')
    duration = models.DurationField('Time Duration')
    active = models.BooleanField('Exam is active', default=False)

    def __str__(self):
        return str(self.exam_name) + ' held on ' + str(self.date)


class McqQuestion(models.Model):
    exam = models.ForeignKey(Exam, models.CASCADE)
    question = models.CharField('The MCQ Question', max_length=50)

    def __str__(self):
        return 'MCQ' + str(self.id) + '<' + str(self.question) + '>'

    def get_choices(self):
        return [(option.answer, option) for option in self.mcqoption_set.all()]


class EssayQuestion(models.Model):
    exam = models.ForeignKey(Exam, models.CASCADE)
    question = models.CharField('The Essay Question', max_length=50)
    working_file = models.FileField('File to work and submit', upload_to='essay_questions/', blank=True, null=True)

    def __str__(self):
        return 'Essay ' + str(self.id) + ' of ' + str(self.exam.exam_name)


class ExamPaper(models.Model):
    student = models.ForeignKey(User, models.CASCADE)
    exam = models.ForeignKey(Exam, models.DO_NOTHING, null=True)
    mcq_marks = models.PositiveIntegerField('Total MCQ paper marks', null=True)
    essay_marks = models.PositiveIntegerField('Total Essay paper marks', null=True)

    def __str__(self):
        return 'Exam Paper ' + 'of ' + str(self.student) + ' for ' + str(self.exam.exam_name)

    def total_marks(self):
        return self.mcq_marks + self.essay_marks


class McqOption(models.Model):
    # exam = models.ForeignKey(ExamPaper, models.DO_NOTHING, blank=True, null=True)
    question = models.ForeignKey(McqQuestion, models.CASCADE, null=False)
    option = models.CharField("Option for Question", max_length=25, null=False)
    is_correct = models.BooleanField("Tick the correct answer", default=False)

    def clean(self):
        super(McqOption, self).clean()
        model = self.question
        if model.mcqoption_set.count() > 4:
            raise ValidationError("Can only create 5 mcq options for '%s'" % model.question)

    def __str__(self):
        return f'Option for MCQ {str(self.question.id)} of {str(self.question.exam.exam_name)}'


class EssayAnswer(models.Model):
    # exam = models.ForeignKey(ExamPaper, models.DO_NOTHING, blank=True, null=True)
    question = models.ForeignKey(EssayQuestion, models.CASCADE, null=False)
    answer = models.FileField("File submitted", null=False, upload_to='essay_answers/')
    marks = models.IntegerField("Marks")

    def __str__(self):
        return f'Answer for Essay {str(self.question.id)} of \
{str(self.paper.student)} for {str(self.paper.exam.exam_name)}'

