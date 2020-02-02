from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import Exam,  McqQuestion, EssayQuestion, McqOption, ExamPaper, EssayAnswer
from .forms import ExamUpdateForm, McqQuestionAddForm, EsyQuestionAddForm
from datetime import timedelta
import random
from .timedexam import TimedExam
from django.contrib.auth.decorators import login_required

# the exam object
EXAM = TimedExam()


@login_required
def home(request):
    mesg, marks = None, None
    if not request.user.is_superuser:
        paper = ExamPaper.objects.filter(student=request.user, exam=EXAM.exam)
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
            'Esys': list(EssayQuestion.objects.filter(exam=exam)),
        })
    else:
        return redirect('home')


@login_required
def remove_question(request, typ, id):
    if request.user.is_superuser and request.is_ajax():
        McqQuestion.objects.get(id=id).delete() if typ == "mcq" else EssayQuestion.objects.get(id=id).delete()
        return HttpResponse("success")
    else:
        return redirect('home')


@login_required
def add_question(request, id, typ, q_id=None):

    def clean_save_new_opt(q):
        for opt in range(1, 5):
            McqOption.objects.create(
                question=q,
                option=request.POST['option_'+str(opt)],
                is_correct='option_'+str(opt) == request.POST['option_correct'],
            )

    def clean_save_old_opt(q):
        for opt in q.get_choices():
            opt.option = request.POST['op_'+str(opt.id)]
            opt.is_correct = 'op_'+str(opt.id) == request.POST['option_correct']
            opt.save()
    
    if request.user.is_superuser:
        exam = Exam.objects.get(id=id)
        form = McqQuestionAddForm if typ == "mcq" else EsyQuestionAddForm
        obj = McqQuestion if typ == "mcq" else EssayQuestion
        q = obj.objects.get(id=q_id) if q_id else None
        ques_form = form(instance=q)
        if request.method == 'POST':
            ques_form = form(request.POST, request.FILES, instance=q)
            if ques_form.is_valid():
                ques_form.exam = exam
                ques_form.save()
                if q and typ == 'mcq':
                    clean_save_old_opt(ques_form.instance)
                    return redirect('view_paper', id)
                elif typ == 'mcq':
                    clean_save_new_opt(q)
                ques_form = form()
        return render(request, 'addquestion.html', {
            'form': ques_form,
            'the_exam': exam,
            'instance': q if q else False,
            'typ': typ,
        })
    else:
        return redirect('home')


@login_required
def admin_dashboard(request):
    if request.user.is_superuser:
        if request.method == 'POST' and not EXAM.status:
            exam = Exam.objects.get(id=int(request.POST['exam'][0]))
            exam.duration = timedelta(seconds=int(request.POST['duration'])*60)
            exam.save()
            EXAM.set_exam(exam)
            EXAM.activate(int(request.POST['duration'])*60)
        elif request.method == 'POST' and EXAM.status:
            EXAM.cancel_out()
        return render(request, 'dashboard.html', {
            'exam_set': Exam.objects.all(),
            'exam': EXAM.exam if EXAM.exam else False,
            'starts': EXAM.cleaned_start(),
            'ends': EXAM.cleaned_over(),
            'over': EXAM.over.strftime("%b %d, %Y %H:%M:%S") if EXAM.status else None,
        })
    else:
        return redirect('home')


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


@login_required
def mcq_paper(request):
    if not EXAM.status:  # or ExamPaper.objects.filter(student=request.user, exam=EXAM.exam):
        return render(request, 'Error_pages/exam_not_found.html')
    elif request.method == 'POST':
        print(request.POST, request.FILES)
        final = dict(request.POST.copy())
        final_files = dict(request.FILES.copy())
        final.pop('csrfmiddlewaretoken')
        points = 0
        for qnum, answ in final.items():
            if qnum.startswith('Es'):
                es = EssayQuestion.objects.get(id=int(qnum[2:]))
                print(es, final_files.keys())
                # EssayAnswer.objects.create(student=request.user, question=es, answer=request.FILES[qnum])
            else:
                question = McqQuestion.objects.get(id=int(qnum))
                if question.get_answer() == McqOption.objects.get(id=int(answ[0])):
                    points += 1
        # ExamPaper.objects.create(student=request.user, exam=EXAM.exam, mcq_marks=points)
        return redirect('home')
    return render(request, 'mcq_sheet.html', {
        'exam': EXAM.exam,
        'MCQs': sorted(list(McqQuestion.objects.filter(exam=EXAM.exam)), key=lambda x: random.random()),
        'Esys': EssayQuestion.objects.all(),
        'over': EXAM.over.strftime("%b %d, %Y %H:%M:%S") if EXAM.status else None
    })


@login_required
def download_essay(request, id, kind):
    file = EssayQuestion.objects.get(id=int(id))
    path = file.working_file.path if kind == 'q' else file.correct_file.path
    try:
        with open(path, 'rb') as f:
            file_data = f.read()
        response = HttpResponse(file_data)
        response['Content-Disposition'] = f'attachment; filename="{file.working_file.name}"'
    except IOError:
        response = HttpResponseNotFound('<h1>File not exist</h1>')
    return response


@login_required
def essay_paper(request):
    if not EXAM.status:
        return render(request, 'Error_pages/exam_not_found.html')
    if request.method == 'POST':
        print(request.POST, request.FILES)
    return render(request, 'essay_sheet.html', {
        'exam': EXAM.exam,
        'Esys': EssayQuestion.objects.all(),
        'over': EXAM.over.strftime("%b %d, %Y %H:%M:%S") if EXAM.status else None
    })
