from django.shortcuts import render,redirect
from .models import Test,Question,Answer,Attempt
import this


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

def attempt_quiz(request):
    testid = request.GET['testid']
    attempt = Attempt()
    attempt.user_id = request.user.username
    attempt.test_id = testid
    attempt.save()
    return redirect('../students/continue_exam?attemptid=' + str(attempt.id) + '&testid=' + str(testid))

def continue_exam(request):

    if(request.method == 'GET'):
        attemptid = request.GET['attemptid']
        testid = request.GET['testid']
        this.questions = Question.objects.all().filter(test_id=testid)
        test = Test.objects.get(id=testid)
        question = this.questions[0]
        this.maximum = len(this.questions)
        return render(request, 'question.html', {'question': question, 'no':1, 'heading':test.name, 'maximum':this.maximum, 'attemptid':attemptid})


    else:

        attemptid = int(request.POST['attemptid'])
        heading = str(request.POST['heading'])
        no = int(request.POST['no'])
        action = request.POST['action']

        if(action == "next" or action == "submit"):
            question = this.questions[no-1]
            try :
                answer = Answer.objects.get(attempt_id=attemptid,question_id=question.id)
            except Answer.DoesNotExist:
                answer = Answer()
            answer.submitted_ans = request.POST['answer']
            answer.attempt_id = attemptid
            answer.question_id = int(question.id)

            if(answer.submitted_ans == question.correct_ans):
                answer.obtained_marks = question.mark
            else:
                answer.obtained_marks = 0

            answer.save()

        if(action == "submit"):
            attempt = Attempt.objects.get(id=attemptid)
            attempt.submitted = True
            attempt.save()
            return redirect('../students/exams')

        if(action == "prev"):
            no = no-2

        question = this.questions[no]
        return render(request, 'question.html', {'question': question, 'no':no+1, 'heading':heading, 'maximum':this.maximum, 'attemptid':attemptid})

