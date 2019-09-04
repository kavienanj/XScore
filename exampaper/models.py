from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    exam_name = models.CharField('The Exam', max_length=25)
    date = models.DateField('Date Held')
    duration = models.DurationField('Time Duration')
    active = models.BooleanField('Exam is active', default=False)

    def __str__(self):
        return str(self.exam_name) + ' held on ' + str(self.date)


class McqQuestions(models.Model):
    class Meta:
        verbose_name = 'MCQ Question'
        verbose_name_plural = 'MCQ Questions'
    exam = models.ForeignKey(Exam, models.CASCADE)
    question = models.CharField('The MCQ Question', max_length=50)
    answer_1 = models.CharField('Answer 1', max_length=25)
    answer_2 = models.CharField('Answer 2', max_length=25)
    answer_3 = models.CharField('Answer 3', max_length=25)
    answer_4 = models.CharField('Answer 4', max_length=25)
    correct = models.CharField('Correct answer', max_length=25)

    def __str__(self):
        return 'MCQ ' + str(self.id) + ' of ' + str(self.exam.exam_name)

    def option_list(self):
        return [self.answer_1, self.answer_2, self.answer_3, self.answer_4]


class EssayQuestion(models.Model):
    exam = models.ForeignKey(Exam, models.CASCADE)
    question = models.CharField('The Essay Question', max_length=50)
    working_file = models.FileField('File to work and submit', upload_to='essay_questions/')

    def __str__(self):
        return 'Essay ' + str(self.id) + ' of ' + str(self.exam.exam_name)


class ExamPaper(models.Model):

    class Meta:
        unique_together = (('student', 'exam'),)

    student = models.ForeignKey(User, models.CASCADE)
    exam = models.ForeignKey(Exam, models.SET_NULL, null=True)
    mcq_marks = models.PositiveIntegerField('Total MCQ paper marks', null=True)
    essay_marks = models.PositiveIntegerField('Total Essay paper marks', null=True)

    def __str__(self):
        return 'Exam Paper ' + 'of ' + str(self.student) + ' for ' + str(self.exam.exam_name)

    def total_marks(self):
        return self.mcq_marks + self.essay_marks


class McqAnswer(models.Model):

    class Meta:
        unique_together = (('paper', 'question'),)

    paper = models.ForeignKey(ExamPaper, models.CASCADE, verbose_name="Exam Paper", null=False)
    question = models.ForeignKey(McqQuestions, models.CASCADE, null=False)
    answer = models.CharField("Answer given", max_length=25, null=False)
    is_correct = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f'Answer for MCQ {str(self.question.id)} of \
{str(self.paper.student)} for {str(self.paper.exam.exam_name)}'


class EssayAnswer(models.Model):

    class Meta:
        unique_together = (('paper', 'question'),)

    paper = models.ForeignKey(ExamPaper, models.CASCADE, verbose_name="Exam Paper", null=False)
    question = models.ForeignKey(EssayQuestion, models.CASCADE, null=False)
    answer = models.FileField("Answer submitted", null=False, upload_to='essay_answers/')
    marks = models.IntegerField("Marks")

    def __str__(self):
        return f'Answer for Essay {str(self.question.id)} of \
{str(self.paper.student)} for {str(self.paper.exam.exam_name)}'

