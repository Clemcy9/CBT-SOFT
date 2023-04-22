from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Discipline, Level, Courses, User,Question, Choice, Result
from .forms import RegisterForm

# Create your views here.

def index(request):
    return HttpResponse('Home Page')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('registration successful')
    else:  
        form = RegisterForm()
    return render(request, 'register.html', {'forms':form})