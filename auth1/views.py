from django.shortcuts import render, HttpResponse, HttpResponseRedirect,redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from cbt_app.models import User
from .forms import RegisterForm, LoginForm
#i love you == i gave him my words and though he disbelieves me, i not back on my words

# Create your views here.

def home(request):
    return render(request, 'home.html',{'user':None})

def login_view(request,next=''):
    # print(request.user.is_authenticated)
    # print(f'user is:{request.user}')
    # if not login already
    if not request.user.is_authenticated:    
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                # password = request.POST['password']
                user = authenticate(email=email, password=password)
                print(f'user =:{user}')
                if user is not None:
                    login(request,user)
                    # must pass the app name into the reverse() for named app url hence 'auth1:profile'
                    if next:
                        print('next provided')
                        return HttpResponseRedirect(next,user)
                    else:
                        print('next not provided')
                        return HttpResponseRedirect(reverse('auth1:profile',args=(user,)))
        else:
            form = LoginForm()
            return render(request, 'login.html', {'forms':form})
    else:
        return redirect(reverse('auth1:profile',args=(request.user,)),permanent=True)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth1:login'))

def register(request):
    print(request.user.is_authenticated)
    # if not login already
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('auth1:login',))
        else:
            form = RegisterForm()
            return render(request, 'register.html', {'forms':form})
    else:
        return redirect(reverse('auth1:profile',args=(request.user,)),permanent=True)
            
@login_required(login_url='/auth/login/')
def profile(request,user):
    id = User.objects.get(email = user)
    print(f'found user is {id}')

    return render(request, 'profile.html',{'user':id or 'no user'})

