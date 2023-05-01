from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.core import serializers
from useful_functions.quiz_result import question_choice_pair, mark_quiz, score
from .models import Discipline, Level, Courses,Question, Choice, Result, Quiz
from .forms import QuizForm

# Create your views here.

def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    # contents = Quiz.objects.filter(level = request.user)
    contents = Quiz.objects.all()
    context = {
        'contents':contents,
    }

    return render(request, 'dashboard.html', context)

@login_required
def take_quiz(request,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    contents = Question.objects.filter(quiz__id = quiz_id).order_by('?')[0:3]
    paginator = Paginator(contents, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'contents':contents,
        'page_obj':page_obj
    }
    return render(request, 'quiz.html', context)



def quiz_progress(request):
    if request.method == 'POST':
        questions = request.POST
        questions= dict(questions)
        print(f'type of quest: {type(questions)}')
        question_pair,question_list =question_choice_pair(questions)
        print(f'quest/choice pair :{question_pair,question_list}')
        result_list =mark_quiz(question_pair,Choice)
        print(f'result is :{result_list}')
        result_percentage = score(result_list,question_list)

        return HttpResponse(f'post received successfully, </br> your result is {result_percentage}')
    