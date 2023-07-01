from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.core import serializers
from django.db import models
from useful_functions.quiz_result import question_choice_pair, mark_quiz, score
from .models import Discipline, Level, Courses,Question, Choice, Result, Quiz,Sitting,UploadTitle
from .forms import QuizForm,QuestionForm
import json
from django.utils.timezone import now

# Create your views here.

def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    # contents = Quiz.objects.filter(level = request.user)
    print('dashboard route running')
    user = request.user
    is_teacher = not user.is_student #not a student
    if is_teacher:
        contents = Quiz.objects.filter(examiner=user)
        sitting = Sitting.objects.filter(quiz__examiner=user)
        quiz_sit_pair ={
            x.quiz:Sitting.objects.filter(quiz=x.quiz).count() for x in sitting 
        }
        context = {
            'contents':contents,
            'sittings':sitting,
            'quiz_pair':quiz_sit_pair,
        }
        return render(request, 'dashboard.html', context)
        

    contents = Quiz.objects.filter(course__in =request.user.profile.courses.all())
    context = {
        'contents':contents,
    }

    return render(request, 'dashboard.html', context)

@login_required
def take_quiz(request,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    sitting = Sitting.sits.check_sitting(request.user,quiz)
    if sitting:
        questions = sitting.get_questions_in_10s().order_by('?')
        time_left =sitting.time_left
        print(f'this is time_left {time_left}, main id is {sitting.id}')
        context={
            'questions':questions,
            'sitting':sitting,
            'time_left':time_left or sitting.quiz.duration
        }
        print(f'this is form {questions}')
        return render(request, 'quiz.html',context)
    else:
        return HttpResponse("You've already taken test")

@login_required
def quiz_progress(request):
    if request.method == 'POST':
        questions = request.POST
        print(f'these are question posted {questions}')
        questions= dict(questions)
        sitting_id = questions['sitting'][0]
        # print(f'sitting id is {sitting_id} and type is {type(sitting_id)}')
        sitting = Sitting.objects.get(id=int(sitting_id))
        print(f'found sitting is {sitting}')
        if sitting:
            question_pair,question_list =question_choice_pair(questions)
            print(f'quest/choice pair :{question_pair}')
            print(f'type of quest pair is: {type(question_pair)}')
            result_list =mark_quiz(question_pair,Choice)
            print(f'result is :{result_list}')
            # result_percentage = score(result_list,question_list)
            sitting.record_attempt(question_list, question_pair)
            sitting.remove_question_in_10s()
            # check if completed quiz
            if (not sitting.question_unattempted) or sitting.time_left <= 0.08: #less than 5secs
                sitting.sitting_complete()
                messages.info(request, f'Quiz completed, your result is {sitting.get_score()}')
                return HttpResponseRedirect(reverse('cbt_app:dashboard'))
            else:
                return(redirect(reverse('cbt_app:take_quiz',args=[sitting.quiz.id])))
        else:
            return HttpResponse('You have completed this quiz b4')
        

        # return HttpResponse(f'post received successfully, </br> your result is {result_percentage}')
    

def api_all_question(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(f'type of jdata:{type(json_data)}\njdata:{json_data}')
        # data = serializers.deserialize()
        return JsonResponse('data received',safe=False)

    question = Question.objects.all().order_by('?')
    choice = Choice.objects.all()
    json_data = serializers.serialize('json',choice)
    # return JsonResponse(json_data,safe=False)
    return HttpResponse(json_data)

def update_timeleft(request, quiz_id):
    if request.method == 'POST':
        # userSitting = Sitting.objects.filter(user =request.user, quiz__id =quiz_id )[0]
        # data = (bytes.decode(request.body,"utf-8"))
        data = json.loads(request.body)
        print(f'post data is {data}')
        userSitting = Sitting.objects.get(id=data['sitting'])
        time_in_min = round(float(data['time'])/60,2) #convert from secs to min
        userSitting.update_time_left(time_in_min)
        print(f'time left now is {userSitting.time_left}, id is {userSitting.id}')
        return HttpResponse('updated time')


def api_edit_quiz(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(f'data from dashboard post = {data}\ntype={type(data["is_active"])}')
        quiz = Quiz.objects.get(id=int(data['quiz_id']))
        quiz.is_available = (data['is_active'].strip(''))
        quiz.save()
        return HttpResponse('ok')
    
@login_required
def result_list(request,quiz_id):
    user = request.user
    if not user.is_student:
        contents = Quiz.objects.filter(examiner=user)
        # sitting = Sitting.objects.filter(quiz__examiner=user)
        sitting = Sitting.objects.filter(quiz__id =quiz_id)
        quiz_sit_pair ={
            x:x.get_score() for x in sitting 
        }
        sits = Sitting.objects.filter(quiz__id =quiz_id)
        total_question =len(sits[0].question_all.split(','))
        total_score = sits.aggregate(models.Sum('current_score'))
        total_attempt =sits.count()
        class_average = round(total_score['current_score__sum'] / total_attempt,2)
        pecertage_class_average = round(class_average/total_question * 100,2)
        print(f'total score ={total_score}\ntotal attempt ={total_attempt}\nclass average={class_average}')
        context = {
            'quiz_attempt':total_attempt,
            'quiz_total_question':total_question,
            'contents':contents,
            'sitting_name':sits[0].quiz.title,
            'quiz_pair':quiz_sit_pair,
            'class_average': class_average,
            'pecertage_class_average': pecertage_class_average
        }
        return render(request, 'result_list.html', context)
        

@login_required
def result_details(request):
    pass