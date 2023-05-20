from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.core import serializers
from useful_functions.quiz_result import question_choice_pair, mark_quiz, score
from .models import Discipline, Level, Courses,Question, Choice, Result, Quiz,Sitting
from .forms import QuizForm,QuestionForm

# Create your views here.

def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    # contents = Quiz.objects.filter(level = request.user)
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
        

    contents = Quiz.objects.all()
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
        context={
            'questions':questions,
            'sitting':sitting,
            'duration':sitting.quiz.duration
        }
        print(f'this is form {questions}')
        return render(request, 'quiz.html',context)
    else:
        return HttpResponse("You've already taken test")
    
@login_required
def quiz_progress(request):
    if request.method == 'POST':
        questions = request.POST
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
            if not sitting.question_unattempted:
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
        json_data = request.POST
        print(f'type of jdata:{type(json_data)}\njdata:{json_data}')
        # data = serializers.deserialize()
        return JsonResponse('data received')

    question = Question.objects.all().order_by('?')
    choice = Choice.objects.all()
    json_data = serializers.serialize('json',choice)
    # return JsonResponse(json_data,safe=False)
    return HttpResponse(json_data)

@login_required
def result_list(request):
    user = request.user
    if not user.is_student:
        contents = Quiz.objects.filter(examiner=user)
        sitting = Sitting.objects.filter(quiz__examiner=user)
        quiz_sit_pair ={
            x:x.get_score() for x in sitting 
        }
        context = {
            'contents':contents,
            'sittings':sitting,
            'quiz_pair':quiz_sit_pair,
        }
        return render(request, 'result_list.html', context)
        

@login_required
def result_details(request):
    pass