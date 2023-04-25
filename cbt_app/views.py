from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Discipline, Level, Courses,Question, Choice, Result, Quiz


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

@login_required
def take_quiz(request,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    contents = Question.objects.filter(quiz__id = quiz_id).order_by('?')
    paginator = Paginator(contents, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'contents':contents,
        'page_obj':page_obj
    }
    return render(request, 'quiz.html', context)