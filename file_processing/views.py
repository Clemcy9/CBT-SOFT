from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import QuestionUploadForm, CourseTemplate
from useful_functions.excel_manipulator import xl2db
from threading import Thread
from create_quiz.views import create_quiz_by_uploads

# Create your views here.

def question_upload(request):
    if request.method == 'POST':
        print(f'request.post contains, {request.POST}')
        print(f'request.user is {request.user}')
        form = QuestionUploadForm(request.POST, request.FILES, user = request.user)
        if form.is_valid():
            print(f'no error: {form.errors}')
            form.save(commit=False)
            form.user = request.user
            title = form.cleaned_data['title']
            file_name = form.cleaned_data['upload']
            course = form.cleaned_data['course']
            duration = form.cleaned_data['duration']
            activate = form.cleaned_data['activate']
            # change the file saving location to user email/the name of file
            form.instance.upload.name = str(course)+ '/' + str(title)+'.'+str(file_name).split('.')[1]
            form.save()
            print(f'title:{title}\nfile_name:{file_name}')
            file_name2 = form.instance.upload
            print(f'title:{title}\nfile_name2:{file_name2}')
            t1 = Thread(target=xl2db, args=[request.user,str(file_name2),course,title])
            t1.start()
            messages.info(request, f'File uploaded successfully, Questions currently being indexed on the background')
            t2 = Thread(target=create_quiz_by_uploads, args=[request.user, title, course, t1,duration,activate])
            t2.start()
            # create_quiz_by_uploads(request.user, title, course,uploading = t1)
            return HttpResponseRedirect(reverse('cbt_app:dashboard'))
        else:
            print(f'error:{request.POST}')
            messages.error(request,'something went wrong')
            # form = QuestionUploadForm(request.POST) 
            return render(request, 'question_upload.html',{'form':form})
    form = QuestionUploadForm(user=request.user)
    
    return render(request, 'question_upload.html',{'form':form})