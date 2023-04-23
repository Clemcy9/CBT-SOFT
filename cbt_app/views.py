from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Discipline, Level, Courses, User,Question, Choice, Result, Quiz
from .forms import RegisterForm

# Create your views here.

def index(request):
    return render(request, 'index.html')
    return HttpResponse('Home Page')

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

@login_required
def take_quiz(request,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    contents = Question.objects.filter(quiz__id = quiz_id).order_by('?')
    context = {
        'contents':contents
    }
    return render(request, 'quiz.html', context)