from django.shortcuts import render
from .models import Test,Question



def exams(request):
    exams = Test.objects.all()
    return render(request, 'exams_results.html', {'pageTitle':'exams','exams': exams})

def results(request):
    exams = ["test1","test2","test3"]
    return render(request, 'exams_results.html', {'pageTitle':'Results','exams': exams})

def exam(request):
    Id = request.GET['id'];
    exam = Test.objects.all().filter(id=Id)
    return render(request, 'exam_result.html', {'exam': exam})

def continue_exam(request):
    Id = request.POST['id']
    no = int(request.POST['no'])
    prev = request.POST['prev']

    if(prev == "true"):
        no = no-2

    questions = Question.objects.all().filter(test_id=Id)
    maximum = len(questions)
    question = questions[no]
    return render(request, 'question.html', {'question': question, 'no':no+1, 'test':Id, 'maximum':maximum})
