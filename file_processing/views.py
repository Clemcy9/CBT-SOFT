from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import QuestionUploadForm, CourseTemplate
from useful_functions.excel_manipulator import xl2db
from threading import Thread

# Create your views here.

def question_upload(request):
    if request.method == 'POST':
        form = QuestionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print(f'no error: {form.errors}')
            form.save(commit=False)
            form.user = request.user
            title = form.cleaned_data['title']
            file_name = form.cleaned_data['upload']
            course = form.cleaned_data['course']
            # change the file saving location to user email/the name of file
            form.instance.upload.name = str(course)+ '/' + str(title)+'.'+str(file_name).split('.')[1]
            form.save()
            print(f'title:{title}\nfile_name:{file_name}')
            file_name2 = form.instance.upload
            print(f'title:{title}\nfile_name2:{file_name2}')
            t1 = Thread(target=xl2db, args=[str(file_name2),course])
            t1.start()
            return HttpResponse(f'successfully Uploaded {file_name2}')
        else:
            print(f'error:{request.POST}')
            messages.error(request,'something went wrong')
            form = QuestionUploadForm(request.POST) 
            return render(request, 'question_upload.html',{'form':form})
    form = QuestionUploadForm()
    
    return render(request, 'question_upload.html',{'form':form})