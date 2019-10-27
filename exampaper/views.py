from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import Exam,  McqQuestion, EssayQuestion  # , McqOption
from .forms import ExamUpdateForm
from datetime import timedelta
from .timedexam import TimedExam
from django.contrib.auth.decorators import login_required

# the exam object
EXAM = TimedExam()


@login_required
def home(request):
    return render(request, 'papers.html')


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


@login_required
def admin_dashboard(request):
    if request.user.is_superuser:
        if request.method == 'POST' and not EXAM.status:
            exam = Exam.objects.get(id=int(request.POST['exam'][0]))
            exam.duration = timedelta(seconds=int(request.POST['duration'][0])*60)
            exam.save()
            EXAM.set_exam(exam)
            EXAM.activate()
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
def mcq_paper(request):
    if not EXAM.status:
        return render(request, 'Error_pages/exam_not_found.html')
    elif request.method == 'POST':
        final = dict(request.POST.copy())
        final.pop('csrfmiddlewaretoken')
        answer_list = []
        # for qnum, answ in final.items():
            # question = McqQuestion.objects.get(id=qnum)
            # answer = McqOption.objects.create(question=question, answer=answ[0])
            # answer_list.append(answer)
        return redirect('home')
    return render(request, 'mcq_sheet.html', {
        'exam': EXAM.exam,
        'MCQs': McqQuestion.objects.all(),
        'over': EXAM.over.strftime("%b %d, %Y %H:%M:%S") if EXAM.status else None
    })


@login_required
def download_essay(request, id):
    if not EXAM.status:
        return HttpResponseNotFound('</br></br><h1><b>Your Exam is not not available now!</b></h1>')
    file = EssayQuestion.objects.get(id=int(id))
    path = file.working_file.path
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
