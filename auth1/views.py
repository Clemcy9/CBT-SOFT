from django.shortcuts import render, HttpResponse, HttpResponseRedirect,redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cbt_app.models import User
from .forms import RegisterForm, LoginForm
#i love you == i gave him my words and though he disbelieves me, i not back on my words

# Create your views here.

# def home(request):
#     return render(request, 'home.html',{'user':None})

def login_view(request):
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
                next1 = request.META['QUERY_STRING']
                next = next1.split(sep='=')[1]
                # ''.split(sep='=')
                print(f'user =:{user}, NEXT1={next}\ntype is:{type(next)}')
                if user is not None:
                    login(request,user)
                    # must pass the app name into the reverse() for named app url hence 'auth1:profile'
                    if next:
                        print('next provided')
                        return HttpResponseRedirect(next,user)
                    else:
                        print('next not provided heeerrrrr')
                        messages.success(request, f'{user} login successfuly \n you can view profile page')
                        # return HttpResponseRedirect(reverse('auth1:profile',args=(user,)))(
                        return HttpResponseRedirect(reverse('cbt_app:index'))
                else:
                    messages.error(request, 'wrong password or email')
                    return render(request, 'login.html', {'forms':form}) 
                    
        else:
            form = LoginForm()
            return render(request, 'login.html', {'forms':form})
    else:
        return redirect(reverse('auth1:profile',args=(request.user,)),permanent=True)


def logout_view(request):
    logout(request)
    messages.info(request, 'successfully logout user')
    return HttpResponseRedirect(reverse('cbt_app:index'))

def register(request):
    print(request.user.is_authenticated)
    # if not login already
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'User registered successful,\n please login')
                print('form is valid')
                return HttpResponseRedirect(reverse('auth1:login',))
            else:
                print(f'form invalid: {form.errors.as_data()}')
                # messages.error(request, form.errors.as_data())
                return render(request, 'register.html', {'forms':form})
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

