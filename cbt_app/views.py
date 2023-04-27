from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from .models import Discipline, Level, Courses,Question, Choice, Result, Quiz
from .forms import QuizForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

'''
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('registration successful')
    else:  
        form = RegisterForm()
    return render(request, 'register.html', {'forms':form})
'''

@login_required
def dashboard(request):
    # contents = Quiz.objects.filter(level = request.user)
    contents = Quiz.objects.all()
    context = {
        'contents':contents,
    }

    return render(request, 'dashboard.html', context)

# @login_required
# def take_quiz(request,quiz_id):
#     quiz = Quiz.objects.get(id=quiz_id)
#     contents = Question.objects.filter(quiz__id = quiz_id).order_by('?')
#     paginator = Paginator(contents, 2)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'contents':contents,
#         'page_obj':page_obj
#     }
#     return render(request, 'quiz.html', context)

@login_required
def take_quiz(request,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    contents = Question.objects.filter(quiz__id = quiz_id).order_by('?')
    paginator = Paginator(contents, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    data = [
         {'question':x.id,} for x in contents
        # {'question':x,'guess':x.choice_set.all()} for x in contents
        # {
        #     'question':'how old was Jesus when he died',
        #     'choices' :[1,23,45,33]

        # }
    ]

    QuizFormSet = formset_factory(QuizForm,extra=5)
    QuizFormSet = QuizFormSet(initial=data)
    context = {
        # 'contents':contents,
        'page_obj':page_obj,
        'formset': QuizFormSet
    }
    return render(request, 'quiz.html', context)



def mark_quiz(result):
    my_result = []
    for choice in result.values():
        is_correct = Choice.objects.get(id=choice).is_answer 
        if is_correct:
            my_result.append(1)
        else:
            my_result.append(0)
        print(f'my_result is : {my_result}')
        return my_result
    
"""
def quiz_progress(request):
    if request.method == 'POST':
        questions = request.POST['questions']
        print(f'questions are {questions}')
        each = [x for x in questions.contents]
        print(f'each is:{each}')
        results = {} #empty dict for storing question and choosen option
        # print(f'this is all data: {request.POST}')
        for question, choice in request.POST:
            results={request.POST.extend}
            results[r'^quest'] = request.POST[r'']


        # for i in range(1,5):
        #     question = request.POST['question'+str(i)]
        #     choice = request.POST['choice'+str(i)]
        #     results[question] = choice
        #     final_results = mark_quiz(results)
        #     return HttpResponse( f'your result is {final_results}')
"""

def quiz_progress(request):
    if request.method == 'POST':
        questions = request.POST['questions']