from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Exam,  McqQuestion, McqOption, ExamPaper
from .forms import ExamUpdateForm, QuestionAddForm
from datetime import timedelta
import random
from datetime import datetime
from .timedexam import TimedExam
from django.contrib.auth.decorators import login_required

# the exam object
EXAM = TimedExam()


@login_required
def home(request):
    mesg, marks = None, None
    if not request.user.is_superuser:
        paper = ExamPaper.objects.filter(student=request.user, exam=EXAM.exam)[0].has_submitted
        if paper:
            mesg = 'Thank You!'
            marks = paper[0].mcq_marks
    return render(request, 'papers.html', {'mesg': mesg, 'marks': marks})


@login_required
def create_paper(request, id=None):
    if request.user.is_superuser:
        exam = id if id is None else Exam.objects.get(id=id)
        exam_form = ExamUpdateForm(instance=exam)
        if request.method == 'POST':
            exam_form = ExamUpdateForm(request.POST, instance=exam)
            if exam_form.is_valid():
                exam_form.save()
                return redirect('dashboard')
        return render(request, 'create_exam.html', {
            'form': exam_form,
        })
    else:
        return redirect('home')


def view_paper(request, id):
    exam = Exam.objects.get(id=id)
    if request.user.is_superuser:
        return render(request, 'viewquestions.html', {
            'exam': exam,
            'MCQs': list(McqQuestion.objects.filter(exam=exam)),
        })
    else:
        return redirect('home')


@login_required
def add_question(request, id, q_id=None, del_q="false"):
    if request.user.is_superuser:
        exam = Exam.objects.get(id=id)
        q = McqQuestion.objects.get(id=q_id) if q_id else None
        if request.is_ajax() and del_q == "true":
            q.delete()
            return HttpResponse("success")
        ques_form = QuestionAddForm(instance=q)
        if request.method == 'POST':
            ques_form = QuestionAddForm(request.POST, request.FILES, instance=q)
            if ques_form.is_valid():
                ques_form.exam = exam
                ques_form.save()
                if q:
                    for opt in q.get_choices():
                        opt.option = request.POST['op_'+str(opt.id)]
                        opt.is_correct = 'op_'+str(opt.id) == request.POST['option_correct']
                        opt.save()
                    return redirect('view_paper', id)
                for opt in range(1, 5):
                    McqOption.objects.create(
                        question=ques_form.instance,
                        option=request.POST['option_'+str(opt)],
                        is_correct='option_'+str(opt) == request.POST['option_correct'],
                    )
                ques_form = QuestionAddForm()
        return render(request, 'addquestion.html', {
            'form': ques_form,
            'the_exam': exam,
            'instance': q if q else False
        })
    else:
        return redirect('home')


@login_required
def mcq_paper(request, id):
    exam = Exam.objects.get(id=id)
    paper = ExamPaper.objects.filter(student=request.user, exam=exam)[0]
    if paper.has_submitted:
        return render(request, 'Error_pages/exam_not_found.html')
    elif request.method == 'POST':
        final = dict(request.POST.copy())
        final.pop('csrfmiddlewaretoken')
        points = 0
        for qnum, answ in final.items():
            question = McqQuestion.objects.get(id=int(qnum))
            if question.get_answer() == McqOption.objects.get(id=int(answ[0])):
                points += 1
        paper.has_submitted = True
        paper.save()
        return redirect('dashboard')
    return render(request, 'mcq_sheet.html', {
        'exam': exam,
        'MCQs': sorted(list(McqQuestion.objects.filter(exam=exam)), key=lambda x: random.random()),
        'over': (datetime.now() + paper.remaining_time).strftime("%b %d, %Y %H:%M:%S")
    })


@login_required
def dashboard(request):
    if request.method == 'POST':
        exam = Exam.objects.get(id=request.POST['exam'])
        if not ExamPaper.objects.filter(student=request.user, exam=exam):
            ExamPaper.objects.create(student=request.user, exam=exam, remaining_time=exam.duration)
        return redirect('mcq', exam.id)
    return render(request, 'dashboard.html', {
        'exam_set': Exam.objects.all(),
    })


@login_required
def results(request, answer_list):
    marks = answer_list.count(True)
    percent = (marks/len(answer_list))*100
    result = {
        'marks': marks,
        'percent': percent,
        'total': len(answer_list),
    }
    return render(request, 'final.html', result)


@login_required
def leader_board(request, id):
    if request.user.is_superuser:
        papers = ExamPaper.objects.filter(exam=Exam.objects.get(id=id))
        if papers:
            papers = papers.order_by('-student')
        return render(request, 'leaderboard.html', {'papers': papers, 'exam': Exam.objects.get(id=id)})
    else:
        return redirect('home')

