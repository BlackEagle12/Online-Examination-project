from django.shortcuts import render,redirect
from .models import Test,Question,Answer,Attempt
import this
from django.utils import timezone


def exams(request):
    if(request.user.is_authenticated):
        class test():
            exam : Test
            compleated : bool

        tests = []
        i = 0

        exams = Test.objects.all().order_by('id')

        attandedExams = Attempt.objects.values_list('test_id').order_by('test_id').filter(user_id=request.user.username,submitted=True)
        attandedExams = list(set(attandedExams))
        for exam in exams:
            temp =  test()
            temp.exam = exam
            if i == len(attandedExams):
                temp.compleated = False
                tests.append(temp)
                continue
            if exam.id == attandedExams[i][0]: #attandedExams[i] is a tuple with one element
                temp.compleated = True
                i = i + 1
            else:
                temp.compleated = False
            tests.append(temp)
        return render(request, 'exams.html', {'pageTitle':'exams','tests': tests})
    else:
        return redirect('../auth/login')

def results(request):
    if(request.user.is_authenticated):
        attandedExams = Attempt.objects.values_list('test_id').order_by('test_id').filter(user_id=request.user.username,submitted=True)
        attandedExams = list(set(attandedExams))
        tests = []
        for exam in attandedExams:
            test = Test.objects.get(id=exam[0]) #exam is a tuple with one element
            tests.append(test)

        return render(request, 'results.html', {'pageTitle':'Results','attandedExams': tests})
    else:
        return redirect('../auth/login')

def exam(request):
    if(request.user.is_authenticated):
        class remTime:
            days : int
            hours : int
            minutes : int
            seconds : int
        Id = request.GET['id'];
        exam = Test.objects.get(id=Id)
        remain = remTime()
        now = timezone.now()
        sub = exam.close - now
        totalSec = sub.seconds
        remain.days = sub.days
        remain.seconds = totalSec % 60
        remain.minutes = (totalSec % 3600)//60
        remain.hours = (totalSec % 216000)//3600

        return render(request, 'exam.html', {'exam': exam, 'remain': remain})
    else:
        return redirect('../auth/login')

def result(request):
    if(request.user.is_authenticated):
        Id = request.GET['id'];
        test = Test.objects.get(id=Id)
        return render(request, 'result.html', {'test': test})
    else:
        return redirect('../auth/login')

def attempt_quiz(request):
    if(request.user.is_authenticated):
        testid = request.GET['testid']
        test = Test.objects.get(id=testid)
        now = timezone.now()
        if (now > test.close):
            note = 'This test has been closed at : ' + str(test.close)
            return render(request, 'error.html', {'note': note, 'heading':test.name})
        elif (now < test.start):
            note = 'This test will open exactly at : ' + str(test.start)
            return render(request, 'error.html', {'note': note, 'heading':test.name})
        elif not test.multipleAttempts:
            try:
                attempt = Attempt.objects.get(user_id=request.user.username,test_id=testid, submitted=True)
                note = 'MultiPle Attempts Are not allowed for this test'
                return render(request, 'error.html', {'note': note, 'heading':test.name})
            except Attempt.DoesNotExist:
                try :
                    attempt = Attempt.objects.get(user_id=request.user.username,test_id=testid, submitted=False)
                except Attempt.DoesNotExist:
                    attempt = Attempt()
                attempt.user_id = request.user.username
                attempt.test_id = testid
                attempt.save()
                return redirect('../students/continue_exam?attemptid=' + str(attempt.id) + '&testid=' + str(testid))

        else :
            try :
                attempt = Attempt.objects.get(user_id=request.user.username,test_id=testid, submitted=False)
            except Attempt.DoesNotExist:
                attempt = Attempt()
            attempt.user_id = request.user.username
            attempt.test_id = testid
            attempt.save()
            return redirect('../students/continue_exam?attemptid=' + str(attempt.id) + '&testid=' + str(testid))
    else:
        return redirect('../auth/login')

def continue_exam(request):
    if(request.user.is_authenticated):
        if(request.method == 'GET'):
            class remTime:
                hours : int
                minutes : int

            remain = remTime()
            remain.hours = 0
            remain.minutes = 2

            attemptid = request.GET['attemptid']
            testid = request.GET['testid']
            this.questions = Question.objects.all().filter(test_id=testid)
            test = Test.objects.get(id=testid)

            if len(this.questions) == 0:
                note = 'THIS QUIZ IS NOT CONFIGURED YET FOR MORE INFORMATION ASK YOUR INSTRUCTOR'
                return render(request, 'error.html', {'note': note, 'heading':test.name, 'attemptid':attemptid})
            else:
                question = this.questions[0]
                this.maximum = len(this.questions)
                return render(request, 'question.html', {'question': question, 'no':1, 'heading':test.name, 'maximum':this.maximum, 'attemptid':attemptid, 'remainWarnings': 5, 'remainTime':remain})

        else:

            class remTime:
                hours : int
                minutes : int

            remain = remTime()
            remainWarnings = int(request.POST['remainWarnings'])
            attemptid = int(request.POST['attemptid'])
            heading = str(request.POST['heading'])
            no = int(request.POST['no'])
            action = request.POST['action']
            remain.hours = request.POST['remainHours']
            remain.minutes = request.POST['remainMinutes']

            if(action == "next" or action == "submit" or action == "prev"):
                question = this.questions[no-1]
                try :
                    answer = Answer.objects.get(attempt_id=attemptid, question_id=question.id)
                except Answer.DoesNotExist:
                    answer = Answer()
                answer.submitted_ans = request.POST.get('answer', "Not Attempted")
                answer.attempt_id = attemptid
                answer.question_id = int(question.id)

                if(answer.submitted_ans == question.correct_ans):
                    answer.obtained_marks = question.mark
                else:
                    answer.obtained_marks = 0

                answer.save()

            if(action == "submit" or remainWarnings < 0):
                attempt = Attempt.objects.get(id=attemptid)
                attempt.submitted = True
                attempt.save()
                return redirect('../students/exams')

            if(action == "prev"):
                no = no-2

            question = this.questions[no]
            return render(request, 'question.html', {'question': question, 'no':no+1, 'heading':heading, 'maximum':this.maximum, 'attemptid':attemptid, 'remainWarnings': remainWarnings, 'remainTime':remain})
    else:
        return redirect('../auth/login')

def testView(request):
    if(request.user.is_authenticated):
        testid = request.GET['testid'];
        test = Test.objects.get(id=testid)
        questions = Question.objects.all().filter(test_id=testid)
        attempts = Attempt.objects.all().filter(test_id=testid, user_id=request.user.username, submitted=True)
        class rows:
            no: int
            question : Question
            answer : Answer

        allattempt = []
        class tables:
            heading: str
            allrows : list
            total : int
            obtain : int

        no = 0
        for x in attempts:
            total = 0
            obtain = 0
            table = tables()
            table.allrows = []

            answers = Answer.objects.all().order_by('question_id').filter(attempt_id=x.id)

            table.heading = "ATTEMPT - " + str(no+1)
            no = no+1
            for i in range(0,len(questions)):
                row = rows()
                row.no = i+1
                row.question = questions[i]
                try:
                    row.answer = answers[i]
                except :
                    row.answer = Answer()
                    row.answer.attempt_id = x.id
                    row.answer.question_id = None
                    row.answer.submitted_ans = "Auto submitted due to illegal activity"
                    row.answer.obtained_marks = 0
                table.allrows.append(row)
                total = total + row.question.mark
                obtain = obtain + row.answer.obtained_marks

            table.total = total
            table.obtain = obtain
            allattempt.append(table)

        return render(request, 'testreview.html', { 'attempts':allattempt, 'heading': test.name })
    else:
        return redirect('../auth/login')