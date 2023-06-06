from django.shortcuts import render, HttpResponse, HttpResponseRedirect,redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Profile, Courses
from .forms import RegisterForm, LoginForm, ProfileForm
#i love you == i gave him my words and though he disbelieves me, i not back on my words

# Create your views here.


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
                next = request.META['QUERY_STRING']
                # a simpler way to get query params with name next
                next11 = request.GET.get('next')
                print(f'this is next.GET(): {next11}')
                
                # ''.split(sep='=')
                print(f'user =:{user}, NEXT1={next}\ntype is:{type(next)}')
                if user is not None:
                    login(request,user)
                    # must pass the app name into the reverse() for named app url hence 'auth1:profile'
                    if next:
                        next = next.split(sep='=')[1]
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
                # form.save()
                # form.save doesnt make the data a valid user hence we use user.create_user to achieve that
                # form.cleaned_data converts it to approved data base format whereas request.POST brings in the raw htmltag value
                # e.g form.cleaned_data of toggle btn = True or False | request.POST = on or off
                print(f"this is form.cleaned_data toggle btn :{form.cleaned_data['is_student']}")
                # print(f"this is request.post toggle btn :{request.POST['is_student']}")

                user = User.objects.create_user(email=form.cleaned_data['email'],first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'],username=form.cleaned_data['username'],is_student = form.cleaned_data['is_student'], password = form.cleaned_data['password'])
                user.save()
                messages.success(request,f'{user} registered successful,\n please login')
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
def profile(request,id):
    # if no profile, create one
    try:
        profile = Profile.objects.get(user__id = id)
        print(f'profile found')
    except:
        profile = Profile(user=request.user)
        print(f'profile created')
        profile.save()
    if request.method =='POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        print(f'error:{form.errors}')
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
            # print(f"post data: {form.cleaned_data['courses']}")
            # profile.phone_number = form.cleaned_data['phone_number']
            # profile.discipline = form.cleaned_data['discipline']
            # profile.courses.add(*[x for x in form.cleaned_data['courses']])
            # profile.current_level = form.cleaned_data['current_level']
            # profile.save()
            # form.save()
            # return HttpResponseRedirect('auth1:profile',args=(request.user,))
            messages.success(request, 'Profile Updated Successfully')
            return redirect(reverse('cbt_app:index'),permanent=True)
          
    
    print(f'this is profile {profile}')
    form = ProfileForm(data=profile.to_dict(), instance=profile)
    context = {
        'profile':profile,
        'form':form,
        'user':request.user
    }
    return render(request, 'profile.html',context)


